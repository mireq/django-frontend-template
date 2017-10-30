#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string
import subprocess
import sys

import fontforge


FONT_FILES_SOURCE_EXTENSIONS = ('.otf', '.woff', '.ttf')
GENERATE_FONTS = ('.ttf', '.woff', '.eot', '.svg', '.woff2')
ALLOWED_CHARS = string.printable + '  ˇ^˘°˛`˙´˝¨\'"¸„“”äáčďéěíľĺňôóřŕšťúůýžÄÁČĎÉĚÍĽĹŇÔÓŘŔŠŤÚŮÝŽ€'
CLEAN_GLYPH_CLASSES = set(['baseglyph', 'baseligature', 'mark'])


def find_font_source_files():
	filenames = [f for f in os.listdir('.') if os.path.isfile(f)]
	scanned_fonts = set()
	font_filenames = []
	for scan_ext in FONT_FILES_SOURCE_EXTENSIONS:
		for fontname in filenames:
			basename, ext = os.path.splitext(fontname)
			if ext.lower() == scan_ext and not basename in scanned_fonts:
				font_filenames.append(fontname)
				scanned_fonts.add(basename)
	return font_filenames


def get_font_properties(fontfile):
	fontname = fontfile.fontname
	familyname = fontfile.familyname
	try:
		basename, fontattrs = fontname.rsplit('-', 1)
	except ValueError:
		basename = fontname
		fontattrs = ''

	font_weight = 400
	italic = False

	if 'Italic' in fontattrs:
		italic = True
		fontattrs = fontattrs.replace('Italic', '')

	if 'Thin' in fontattrs or 'Hairline' in fontattrs or '100' in fontattrs:
		font_weight = 100
	elif 'Extralight' in fontattrs or 'Ultralight' in fontattrs or '200' in fontattrs:
		font_weight = 200
	elif 'Semibold' in fontattrs or 'Demibold' in fontattrs or '600' in fontattrs:
		font_weight = 600
	elif 'Extrabold' in fontattrs or 'Ultrabold' in fontattrs or '800' in fontattrs:
		font_weight = 800
	elif 'Light' in fontattrs or '300' in fontattrs:
		font_weight = 300
	elif 'Normal' in fontattrs or '400' in fontattrs:
		font_weight = 400
	elif '500' in fontattrs:
		font_weight = 500
	elif 'Bold' in fontattrs or '700' in fontattrs:
		font_weight = 700
	elif 'Black' in fontattrs or '900' in fontattrs:
		font_weight = 900

	return {
		'basename': basename,
		'familyname': familyname,
		'attrs': fontattrs,
		'font_weight': font_weight,
		'italic': italic,
	}


def write_scss_font(fontfile, sourcename, fp):
	basename = os.path.splitext(sourcename)[0]
	if len(sys.argv) > 1:
		basename = sys.argv[1] + basename
	properties = get_font_properties(fontfile)
	fp.write("@font-face {\n");
	fp.write("\tfont-family: '%s';\n" % properties['basename']);
	fp.write("\tfont-weight: %d;\n" % properties['font_weight']);
	fp.write("\tfont-style: %s;\n" % ('italic' if properties['italic'] else 'normal'));
	fp.write("\tsrc: url('%s.eot');\n" % basename)
	localfontnames = []
	localfontnames.append(properties['basename'] + ' ' + properties['attrs'] if properties['attrs'] else properties['basename'])
	localfontnames.append(properties['basename'] + '-' + properties['attrs'] if properties['attrs'] else properties['basename'])
	localfontnames.append(properties['familyname'])
	fp.write("\tsrc: local('%s'), local('%s'), local('%s'),\n" % tuple(localfontnames))
	fp.write("\t\turl('%s.eot?#iefix') format('embedded-opentype'),\n" % basename)
	fp.write("\t\turl('%s.woff2') format('woff2'),\n" % basename)
	fp.write("\t\turl('%s.woff') format('woff'),\n" % basename)
	fp.write("\t\turl('%s.ttf') format('truetype'),\n" % basename)
	fp.write("\t\turl('%s.svg?#%s') format('svg');\n" % (basename, properties['attrs'] if properties['attrs'] else 'Regular'))
	fp.write("}\n\n");


def minimalize_font(font):
	for char in ALLOWED_CHARS:
		font.selection[ord(char)] = True
	font.selection.invert()
	for i in font.selection.byGlyphs:
		if i.glyphclass in CLEAN_GLYPH_CLASSES:
			font.removeGlyph(i)


def main():
	with open('_fonts.scss', 'w') as scss_fp:
		for filename in find_font_source_files():
			fontfile = fontforge.open(filename)
			for suffix in GENERATE_FONTS:
				if suffix == '.woff2':
					subprocess.call(['woff2_compress', os.path.splitext(filename)[0] + '.ttf'], stdout=subprocess.PIPE)
				else:
					font_output = os.path.splitext(filename)[0] + suffix
					if ALLOWED_CHARS is not None:
						minimalize_font(fontfile)
					fontfile.generate(font_output)
			write_scss_font(fontfile, filename, scss_fp)


if __name__ == "__main__":
	main()
