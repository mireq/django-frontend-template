#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from collections import OrderedDict
import argparse
import os
import string
import subprocess
import sys

import fontforge


FONT_FILES_SOURCE_EXTENSIONS = ('.otf', '.woff', '.ttf')
#GENERATE_FONTS = ('.ttf', '.woff', '.eot', '.svg', '.woff2')
GENERATE_FONTS = ('.ttf', '.woff', '.woff2')
ALLOWED_CHARS = string.printable + '  ˇ^˘°˛`˙´˝¨\'"¸„“”äáčďéěíľĺňôóřŕšťúůýžÄÁČĎÉĚÍĽĹŇÔÓŘŔŠŤÚŮÝŽ€§'
CLEAN_GLYPH_CLASSES = set(['baseglyph', 'baseligature', 'mark', 'automatic'])


def make_uniqe_list(iterable):
	return list(OrderedDict.fromkeys(iterable))


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

	if 'Thin' in fontattrs or 'Hairline' in fontattrs or '100' in fontattrs:
		font_weight = 100
	elif 'Extralight' in fontattrs or 'Ultralight' in fontattrs or 'ExtraLight' in fontattrs or 'UltraLight' in fontattrs or '200' in fontattrs:
		font_weight = 200
	elif 'Extrabold' in fontattrs or 'Ultrabold' in fontattrs or 'ExtraBold' in fontattrs or 'UltraBold' in fontattrs or '800' in fontattrs:
		font_weight = 800
	elif 'Light' in fontattrs or '300' in fontattrs:
		font_weight = 300
	elif 'Normal' in fontattrs or 'Book' in fontattrs or 'Regular' in fontattrs or '400' in fontattrs:
		font_weight = 400
	elif 'Medium' in fontattrs or '500' in fontattrs:
		font_weight = 500
	elif 'Semibold' in fontattrs or 'Demibold' in fontattrs or 'SemiBold' in fontattrs or '600' in fontattrs:
		font_weight = 600
	elif 'Bold' in fontattrs or '700' in fontattrs:
		font_weight = 700
	elif 'Black' in fontattrs or 'Heavy' in fontattrs or '900' in fontattrs:
		font_weight = 900

	return {
		'basename': basename,
		'familyname': familyname,
		'attrs': fontattrs,
		'font_weight': font_weight,
		'italic': italic,
	}


def write_scss_font(fontfile, sourcename, fp, args):
	properties = get_font_properties(fontfile)
	basename = os.path.splitext(sourcename)[0]
	if args.static_prefix:
		basename = args.static_prefix + basename
	font_family = properties['basename']
	if args.font_family:
		font_family = args.font_family
	fp.write("@font-face {\n")
	fp.write("\tfont-family: '%s';\n" % font_family)
	fp.write("\tfont-weight: %d;\n" % properties['font_weight'])
	fp.write("\tfont-style: %s;\n" % ('italic' if properties['italic'] else 'normal'))
	fp.write("\tfont-display: swap;\n")
	if '.eot' in GENERATE_FONTS:
		fp.write("\tsrc: url(static('%s.eot'));\n" % basename)
	localfontnames = []
	localfontnames.append(properties['basename'] + ' ' + properties['attrs'] if properties['attrs'] else properties['basename'])
	localfontnames.append(properties['basename'] + '-' + properties['attrs'] if properties['attrs'] else properties['basename'])
	localfontnames.append(properties['familyname'])
	localfontnames.append(properties['basename'])
	localfontnames = ["local('%s')" % name for name in make_uniqe_list(localfontnames)]
	fp.write("\tsrc: %s" % ', '.join(localfontnames))
	if '.eot' in GENERATE_FONTS:
		fp.write(",\n\t\turl(#{static(\"%s.eot\")}?#iefix) format('embedded-opentype')" % basename)
	if '.woff2' in GENERATE_FONTS:
		fp.write(",\n\t\turl(static('%s.woff2')) format('woff2')" % basename)
	if '.woff' in GENERATE_FONTS:
		fp.write(",\n\t\turl(static('%s.woff')) format('woff')" % basename)
	if '.ttf' in GENERATE_FONTS:
		fp.write(",\n\t\turl(static('%s.ttf')) format('truetype')" % basename)
	if '.svg' in GENERATE_FONTS:
		fp.write(",\n\t\turl(#{static(\"%s.svg\")}?#%s) format('svg')" % (basename, properties['attrs'] if properties['attrs'] else 'Regular'))
	fp.write(";\n}\n\n")


def minimalize_font(font):
	for char in ALLOWED_CHARS:
		font.selection[ord(char)] = True
	font.selection.invert()
	for i in font.selection.byGlyphs:
		if i.glyphclass in CLEAN_GLYPH_CLASSES:
			font.removeGlyph(i)


def main():
	parser = argparse.ArgumentParser(description="Generate web fonts")
	parser.add_argument('--static_prefix', help="Generate with prefix (starting from /static/ directory)")
	parser.add_argument('--font_family', help="Set font family")
	args = parser.parse_args()

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
			write_scss_font(fontfile, filename, scss_fp, args)


if __name__ == "__main__":
	main()
