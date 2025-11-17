#!/usr/bin/env python3

PRINTER = '/dev/usb/lp0'  # the printer device

DOTS_MM = 8  # printer dots per mm, 8 == 203 dpi
WIDTH_MM = 100  # sticker width, mm
HEIGHT_MM = 35  # sticker height, mm
GAP_MM = 2  # sticker gap, mm

FONT = "0"  # built-in vector font, scalable by X and Y
FONT_WIDTH = 36  # font width, in points, reduce to make letters narrower
FONT_HEIGHT = 36  # font height, in points
FONT_X_MULT = FONT_WIDTH  # font multiplication, for "0" font is size in points
FONT_Y_MULT = FONT_HEIGHT  # font multiplication, for "0" font is size in points

BADGE_GAP_MM = 5  # initial gap from the sticker start, mm
LINES_GAP_MM = 1  # gap between lines, mm

PREVIEW_WIDTH = 16  # width of the preview in symbols


import os
import sys
import time
import argparse
import re


def main(args):
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dry-run', action='store_true', default=False, help='do not print actually')
    ap.add_argument('-y', '--yes', action='store_true', default=False, help='print without confirmation')
    ap.add_argument('-n', '--num', type=int, default=1, help='number of similar badges to print')
    ap.add_argument('-o', '--orient', type=int, choices=[0, 1], default=1,
                    help='orientation: 1 - human-friendly, 0 - paper-friendly')
    ap.add_argument('line1', nargs='?', default='')
    ap.add_argument('line2', nargs='?', default='')

    params = ap.parse_args(args)

    params.line1 = re.sub(r'[\n\r]+', '', params.line1)
    params.line2 = re.sub(r'[\n\r]+', '', params.line2)

    try:
        confirm = Confirm(params)
        if params.yes or confirm.confirm():
            badge = Badge(params)
            printer = Printer(params, badge)
            printer.print()
    except Exception as e:
        print(e, file=sys.stderr)


class Confirm:

    def __init__(self, params):
        self.params = params

    @staticmethod
    def print_line_centered(line):
        spaces = (PREVIEW_WIDTH - len(line)) // 2
        print(' ' * spaces, line, sep='')

    def confirm(self):
        print('-' * PREVIEW_WIDTH)
        for i in range(0, self.params.num):
            self.print_line_centered(self.params.line1)
            self.print_line_centered(self.params.line2)
        print('-' * PREVIEW_WIDTH)

        reply = input('Print? [Y/n] ')
        print()
        if len(reply) > 0 and reply[0] in ('y', 'Y'):
            return True
        elif reply == '':
            return True
        else:
            return False


class Badge:
    width = WIDTH_MM * DOTS_MM
    x_center = width // 2
    y_first_line = BADGE_GAP_MM * DOTS_MM  # Y position of the first line (top of the line)
    line_height = (FONT_HEIGHT // 3 + LINES_GAP_MM) * DOTS_MM  # line height in pixels
    y_second_line = y_first_line + line_height  # Y position of the second line (top of the line)

    def __init__(self, params):
        self.line1 = params.line1
        self.line2 = params.line2

    def print(self):
        commands = [
            'CLS',
            'TEXT {x},{y},"{font}",0,{font_x_mult},{font_y_mult},2,"{text}"'.format(
                x=self.x_center, y=self.y_first_line,
                font=FONT, font_x_mult=FONT_X_MULT, font_y_mult=FONT_Y_MULT,
                text=self.line1),
            'TEXT {x},{y},"{font}",0,{font_x_mult},{font_y_mult},2,"{text}"'.format(
                x=self.x_center, y=self.y_second_line,
                font=FONT, font_x_mult=FONT_X_MULT, font_y_mult=FONT_Y_MULT,
                text=self.line2)
        ]
        return commands


class Printer:
    width = WIDTH_MM * DOTS_MM
    height = HEIGHT_MM * DOTS_MM

    def __init__(self, params, badge):
        self.params = params
        self.badge = badge
        if not self.params.dry_run:
            self.printer = os.open(PRINTER, os.O_RDWR)

    def printer_status(self):
        os.write(self.printer, b"\x1B!S\r\n")
        status = os.read(self.printer, 8)
        return status[1:5].decode('ascii')

    def can_print(self):
        return re.fullmatch(r'[@BCFPW]@@@', self.printer_status()) is not None

    def wait_printer(self):
        if self.params.dry_run:
            return

        if not self.can_print():
            print('...waiting printer...', end='', file=sys.stderr)
            time.sleep(0.5)
            while not self.can_print():
                print('.', end='', file=sys.stderr)
                time.sleep(1)
            print(file=sys.stderr)

    def page_setup(self):
        self.command('SIZE {} mm,{} mm'.format(WIDTH_MM, HEIGHT_MM))
        self.command('GAP {} mm,0 mm'.format(GAP_MM))
        self.command('CODEPAGE UTF-8')
        self.command('DIRECTION {}'.format(self.params.orient))

    def print(self):
        self.wait_printer()
        self.page_setup()

        for cmd in self.badge.print():
            self.command(cmd)

        self.command('PRINT 1,{}'.format(self.params.num))

        print(self.badge.line1, self.badge.line2)

    def command(self, cmd):
        if self.params.dry_run:
            print(cmd)
        else:
            os.write(self.printer, cmd.encode('utf-8'))
            os.write(self.printer, b'\r\n')


if __name__ == '__main__':
    main(sys.argv[1:])

