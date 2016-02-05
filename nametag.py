import sys
import shutil
import requests
import subprocess
from PIL import Image, ImageDraw, ImageFont


def make_tag(name, github, tag_w, tag_h):

    ratio = tag_w / tag_h

    # Colours
    white = (255, 255, 255)
    black = (39, 39, 39)

    # Fonts
    FONT_PATH = '/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-C.ttf'
    FONT_SIZE = 380
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Open image
    base_image = 'ads_partial_logo_dark_background.jpg'
    base_im = Image.open(base_image)

    base_image_w = base_im.size[0]
    base_image_h = base_im.size[1]

    # Image should be padded to ensure ratio of 2:1 for width:height
    padding_w = int(ratio*base_image_w)
    padding_h = int(base_image_h)

    # Make the padding
    padding_im = Image.new('RGB', (padding_w, padding_h), white)
    padding_im.paste(base_im, base_im.getbbox())

    # Figure out layout of the name
    new_name = name.split(' ')
    if None:
        name_length = len(new_name)
        name_seperation = int(padding_h / (1.0*name_length))
    name_seperation = FONT_SIZE

    # Draw the name on the image
    draw = ImageDraw.Draw(padding_im)
    start_y = 150
    start_x = base_image_w + 100
    for text in new_name:
        text_position = (start_x, start_y)
        draw.text(text_position, text, black, font)

        start_y += name_seperation

    # Add faces
    circle_x = 538
    circle_y = 207
    radius = 145
    github_img_x = circle_x - radius
    github_img_y = circle_y - radius

    if github:
        # Look up face on github
        github_file = '{}.jpeg'.format(github)
        github_url = 'https://api.github.com/users/{}'.format(github)

        import os

        got_github = False
        if not os.path.isfile('{}/{}'.format(os.getcwd(), github_file)):
            print 'Looking up GitHub url: {}'.format(github_url)
            r = requests.get(github_url)
            try:
                avatar_url = r.json()['avatar_url']
                r = requests.get(avatar_url, stream=True)
                with open(github_file, 'wb') as github_image:
                    shutil.copyfileobj(r.raw, github_image)

                print 'GitHub image from GitHub: {}'.format(github_file)
                print r
                del r

                got_github = True

            except KeyError:
                pass
        else:
            print 'GitHub image locally: {}'.format(github_file)
            got_github = True

        if got_github:

            github_im = Image.open(github_file)
            github_im.thumbnail((radius*2, radius*2), Image.ANTIALIAS)

            mask = Image.new('L', github_im.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + github_im.size, fill=255)

            padding_im.paste(github_im, (github_img_x, github_img_y), mask=mask)

    # Save image
    name = name.replace(' ', '_').replace('.', '_')
    output_image = '{}-name-tag.jpg'.format(name)
    padding_im.save(output_image)

    # Information to the user
    print 'Input image had width/height: {} x {}'.format(base_image_w, base_image_h)
    print 'Padding adding to give width/height: {} x {}'.format(padding_w, padding_h)
    print 'Text:'
    print '\t"{}"'.format(text)
    print '\tfont "{}" with size "{}"'.format(FONT_PATH, FONT_SIZE)
    print '\tposition "{}"'.format(text_position)
    print 'Output file: {}'.format(output_image)

    return output_image

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--person', nargs='*', action='append', help='Usage: -p <name>, <github handle> [handle optional]')

    args = parser.parse_args()
    if not args.person:
        print parser.print_help()
        sys.exit()

    person_list = []
    for person in args.person:

        p = ' '.join(person).split(',')
        person_dict = {}
        person_dict['name'] = p[0]

        try:
            person_dict['github'] = p[1].replace(' ', '')
        except IndexError:
            pass
        person_list.append(person_dict)

    latex = [
        '\documentclass[11pt]{letter}',
        '\usepackage{graphicx}',
        '\usepackage{geometry}',
        '\geometry{left=5cm,top=2cm,right=1cm,bottom=1cm}'
        '\\begin{document}',
    ]

    # Measurement of size of tags
    tag_w = 10.5 # cm
    tag_h = 5.1 # cm

    # Build the latex
    counter = 1
    for person in person_list:
        print 'Running on person: {}'.format(person)
        img_name = make_tag(name=person['name'], github=person.get('github', None), tag_w=tag_w, tag_h=tag_h)

        latex.append('    \\frame{{\includegraphics[width={}cm]{{{}}}}}'
                     .format(tag_w, img_name))
        latex.append('    ' + '\\newline'*5)

    latex.append('\end{document}')

    print 'LaTeX built'
    print 'Compiling LaTeX'

    output_latex = 'name_tags.tex'
    with open(output_latex, 'w') as out_f:
        out_f.write('\n'.join(latex))

    # Compile the latex
    process = subprocess.Popen(['pdflatex', output_latex], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    print 'PDFLaTeX output: {}'.format(out)
    print 'PDFLaTeX error: {}'.format(err)






























