from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4 import QtCore
import sys
import struct
import time


class MintGui(QtGui.QWidget):
    """
    MintGui class

    Display a hex view of a memory range, including coloring of address ranges.
    """

    #
    # Constants
    #


    # Text/Hex display header rows
    TEXT_DISPLAY_HEADER = 'Text Display'
    ADDRESS_DISPLAY_HEADER = 'Address'


    # Number of characters to display for address view
    ADDRESS_DISPLAY_WIDTH = 8
    # Number of characters to display for hex view
    HEX_DISPLAY_WIDTH = (4 * 2) + 1
    # Number of characters to display for text view
    TEXT_DISPLAY_WIDTH = len(TEXT_DISPLAY_HEADER) + 2

    __app_instance = None


    def __init__(self, data, start_address = 0x0, item_size = 4, color_ranges = [], parent = None):
        """
            data - Binary blob of data to display
            start_address - The virtual address where the data starts
            item_size - 1, 2 or 4 bytes per item (can be set using setItemSize method)
            color_ranges - A list of color ranges, where each color range is (start_addr, end_addr, color) - (can be set using setColorsRanges method)
        """

        if (QtGui.QApplication.instance() is None):
            MintGui.__app_instance = QtGui.QApplication(sys.argv)

        QtGui.QWidget.__init__(self, parent)

        #
        # Class members
        #

        self._data = data
        self._start_address = start_address

        if (item_size not in [1,2,4]):
            raise Exception("Item size must be 1, 2 or 4")
        self._item_size = item_size

        self._color_ranges = color_ranges
        self._getAbsoluteColorAddresses()

        self._items_per_row = 0

        self._window_title_set = False

        #
        # Initialize the components of the window
        #

        self.display_font = QtGui.QFont("Courier New", 10)


        #
        # Address Display
        #

        self.address_display = QtGui.QTextEdit()
        address_display_width = self._calcStringWidth(MintGui.ADDRESS_DISPLAY_WIDTH + 2)
        self.address_display.setMaximumWidth(address_display_width)
        self.address_display.setMinimumWidth(address_display_width)
        self.address_display.setReadOnly(True)
        self.address_display.setCurrentFont(self.display_font)
        self.address_display.setWordWrapMode(False)


        #
        # Hex Display
        #

        self.hex_display = QtGui.QTextEdit()
        self.hex_display.setReadOnly(True)
        self.hex_display.setCurrentFont(self.display_font)
        self.hex_display.setMinimumWidth(self._calcStringWidth(MintGui.HEX_DISPLAY_WIDTH + 2))
        self.hex_display.setWordWrapMode(False)

        #
        # Text Display
        #

        self.text_display = QtGui.QTextEdit("")
        self.text_display.setReadOnly(True)
        self.text_display.setCurrentFont(self.display_font)
        self.text_display.setMinimumWidth(self._calcStringWidth(MintGui.TEXT_DISPLAY_WIDTH + 1))
        self.text_display.setWordWrapMode(False)


        #
        # Vertical Scrollbar
        #

        self.scrollbar = QtGui.QScrollBar(Qt.Vertical, self)
        self.scrollbar.sliderChange = self._onSliderChange
        
        #
        # Horizontal Layout
        #

        self.horizontal_layout = QtGui.QHBoxLayout()

        self.horizontal_layout.addWidget(self.address_display, 1)
        self.horizontal_layout.addWidget(self.hex_display, 2)
        self.horizontal_layout.addWidget(self.text_display, 1)
        self.horizontal_layout.addWidget(self.scrollbar, 1)

        self.setLayout(self.horizontal_layout)

        self._updateContentDisplayRatio()

        #
        # Window size and title
        #

        self.setGeometry(300, 300,
                self.hex_display.minimumWidth() + self.address_display.minimumWidth() + self.text_display.minimumWidth() + 50,
                150)

        self.setWindowTitle('PyMint: %X - %X' % (start_address, start_address + len(data)))




        # Refresh the content of the window
        self.resizeEvent(None)


    #
    # Events
    #


    def resizeEvent(self, ev):
        item_width = self._calcStringWidth((self._item_size * 2) + 1)
        hex_display_width = self.hex_display.width()

        old_items_per_row = self._items_per_row
        self._items_per_row = (hex_display_width / item_width)

        # Refresh the scroll bar
        row_height = QtGui.QFontMetrics(self.display_font).lineSpacing()
        total_rows = len(self._data) / (self._items_per_row * self._item_size)
        window_height = self.height()
        self._visible_rows = (window_height / row_height) - 3

        old_value = self.scrollbar.value() * 1.0
        old_max = self.scrollbar.maximum()
        scrollbar_ratio = (old_value / old_max) if (old_max > 0) else 0

        new_max = (total_rows - self._visible_rows) + 1
        if (new_max < 0): new_max = 0
        self.scrollbar.setMaximum(new_max)
        self.scrollbar.setMinimum(0)
        self.scrollbar.setSingleStep(1)
        self.scrollbar.setValue(new_max * scrollbar_ratio)

        if (old_items_per_row != self._items_per_row):
            self._formatData(
                self._data,
                self._start_address,
                self._item_size,
                self._items_per_row
                )



        self._refreshContent()

    def _onSliderChange(self, changeType):
        self.scrollbar.update()
        if (changeType == QtGui.QSlider.SliderRangeChange):
            pass
        elif (changeType == QtGui.QSlider.SliderValueChange):
            self._refreshContent()

        if (self.scrollbar.value() >= 10):
            new_data = 'bobo' * 1000
            self.setData(new_data, 0x30000)

    def _refreshContent(self):
        index = self.scrollbar.value()
        end_index = index + self._visible_rows

        self._setHeaderLine(self.address_display, ("%-#8s") % MintGui.ADDRESS_DISPLAY_HEADER)
        self.address_display.append('\n'.join(self._address_display[index: end_index]))

        self._setHeaderLine(self.hex_display, self._hex_column_line)

        self._insertColoredLines(self.hex_display,
                self._hex_display[index: end_index],
                self._hex_display_colors[index: end_index])

        self._setHeaderLine(self.text_display, ("%-#" + str(self._items_per_row * self._item_size) + "s") % MintGui.TEXT_DISPLAY_HEADER)

        self._insertColoredLines(self.text_display,
                self._text_display[index: end_index],
                self._text_display_colors[index: end_index])


    #
    # Setters/Getters
    #


    def setColorsRanges(self, color_ranges):
        """
        Sets the color ranges of the data to display.

        color_ranges - A list of color ranges, where each color range is (start_addr, end_addr, color)
        """
        self._color_ranges = color_ranges

        # Convert color ranges into absolute values
        self._getAbsoluteColorAddresses()

        # Refresh content
        self._formatData(
            self._data,
            self._start_address,
            self._item_size,
            self._items_per_row
            )

        self._refreshContent()


    def getColorsRanges(self):
        """
        Gets the list of color ranges
        """

        return self._color_ranges


    def setItemSize(self, new_size):
        """
        Sets the item size (1, 2 or 4 bytes)
        """

        if (new_size not in [1,2,4]):
            raise Exception("Item size must be 1, 2 or 4")

        self._item_size = new_size

        self.scrollbar.setValue(0)

        # Refresh content
        self.resizeEvent(None)

        self._updateContentDisplayRatio()


    def getItemSize(self):
        """
        Gets item size (1, 2 or 4 bytes)
        """

        return self._item_size


    def setData(self, data, start_address):
        """
        Sets the data and start address to display
        """

        self._data = data
        self._start_address = start_address
        self._color_ranges = []
        self._getAbsoluteColorAddresses()

        self._items_per_row = 0
        self.resizeEvent(None)

        if (self._window_title_set == False):
            # Refresh the window title only if it hasn't been set externally
            self.setWindowTitle('PyMint: %X - %X' % (start_address, start_address + len(data)))


    def setTitle(self, title):
        """
        Sets the window title
        """

        self.setWindowTitle(title)
        self._window_title_set = True

    def getTitle(self):
        """
        Gets the window title
        """

        return self.windowTitle()


    #
    # Helper functions
    #


    def _insertColoredLines(self, text_box, lines, colors):
        for i in xrange(len(lines)):
            line = lines[i]
            color_ranges = colors[i]

            if (not color_ranges):
                # No special coloring needed
                text_box.append(line)
                continue

            text_box.append('')

            i = 0
            for color_range in color_ranges:
                cur = text_box.textCursor()
                cur.movePosition(QtGui.QTextCursor.End)
                text_box.setTextCursor(cur)

                text_box.setTextBackgroundColor(QtGui.QColor('white'))
                text_box.insertPlainText(line[i: color_range[0]])

                cur = text_box.textCursor()
                cur.movePosition(QtGui.QTextCursor.End)
                text_box.setTextCursor(cur)
                text_box.setTextBackgroundColor(QtGui.QColor(color_range[1]))
                text_box.insertPlainText(line[color_range[0]: color_range[0] + 1])
                i = color_range[0] + 1

            text_box.setTextBackgroundColor(QtGui.QColor('white'))
            text_box.insertPlainText(line[i:])


    def _formatData(self, table, base = 0, itemSize=4, itemsInRow = 0x8 ):
        # Prepare the first row (which contains columns of offsets within each line)
        itemStr = '%%-%dx' % (itemSize * 2)
        hex_column_line = ''
        for i in range(itemsInRow):
            hex_column_line += itemStr % (i * itemSize)
            hex_column_line += ' '
        self._hex_column_line = hex_column_line[:-1]

        # Format the text of the various displays
        (self._address_display,
                (self._hex_display, self._hex_display_colors),
                (self._text_display, self._text_display_colors)) = \
                self._formatTable(
                        self._data,
                        self._start_address,
                        self._item_size,
                        self._items_per_row,
                        )


    def _formatTable(self, table, base = 0, itemSize=4, itemsInRow = 0x8 ):
        address_data = []
        hex_data = []
        hex_data_colors = []
        string_data = []
        string_data_colors = []

        address_format = '%0' + str(MintGui.ADDRESS_DISPLAY_WIDTH) + 'x'

        if (itemSize == 1):
            size_format = 'B'
        elif (itemSize == 2):
            size_format = 'H'
        elif (itemSize == 4):
            size_format = 'L'

        itemHex = '%%0%dx' % (itemSize * 2)

        for i in xrange(0, len(table), itemsInRow * itemSize):

            if 0 == base:
                address_data.append(address_format % (i))
            else:
                address_data.append(address_format % (i + base))

            raw_line_data = table[i:][:itemsInRow * itemSize]

            # Convert from single bytes to larger items (1/2/4 bytes)
            line_data = []
            for c in xrange(0, len(raw_line_data), itemSize):
                line_data.append(struct.unpack_from('=' + size_format, raw_line_data, c)[0])

            hex_line = ''
            current_offset = i + base
            current_color_range = []
            for t in line_data:
                line_offset = len(hex_line)

                for addr in xrange(current_offset, current_offset + itemSize):
                    if (self._absolute_color_addresses.has_key(addr)):
                        # Since each byte is actually 2 hex characters wide
                        current_color_range.append([(itemSize - (addr - current_offset) - 1) * 2 + line_offset, self._absolute_color_addresses[addr]])
                        current_color_range.append([(itemSize - (addr - current_offset) - 1) * 2 + line_offset + 1, self._absolute_color_addresses[addr]])

                hex_line += itemHex % t
                hex_line += ' '

                current_offset += itemSize

            current_color_range.sort(cmp = lambda x,y: cmp(x[0], y[0]))
            hex_data_colors.append(current_color_range)
            hex_data.append(hex_line.rstrip())

            string_line = ''
            current_offset = i + base
            current_color_range = []
            for t in line_data:
                for x in struct.pack('=' + size_format, t):
                    line_offset = len(string_line)

                    if (self._absolute_color_addresses.has_key(current_offset)):
                        current_color_range.append([line_offset, self._absolute_color_addresses[current_offset]])

                    if( x == `x`[1] ):
                        string_line += x
                    else:
                        string_line += '.'

                    current_offset += 1

            current_color_range.sort(cmp = lambda x,y: cmp(x[0], y[0]))
            string_data_colors.append(current_color_range)
 
            string_data.append(string_line.rstrip())

        return (address_data, (hex_data, hex_data_colors), (string_data, string_data_colors))




    def _calcStringWidth(self, length):
        # Assume fixed-size font
        return QtGui.QFontMetrics(self.display_font).width('X' * length)


    def _setHeaderLine(self, text_box, line):
        text_box.setFontWeight(QtGui.QFont.Bold)
        text_box.setFontUnderline(True)
        text_box.setText(line)

        text_box.setFontWeight(QtGui.QFont.Normal)
        text_box.setFontUnderline(False)
 
    def _getAbsoluteColorAddresses(self):
        self._absolute_color_addresses = {}
        for (start_addr, end_addr, color) in self._color_ranges:
            for addr in xrange(start_addr, end_addr + 1):
                self._absolute_color_addresses[addr] = color


    def _updateContentDisplayRatio(self):
        if (self._item_size == 1):
            hex_display_ratio = 5
            text_display_ratio = 2

        elif (self._item_size == 2):
            hex_display_ratio = 15
            text_display_ratio = 7

        elif (self._item_size == 4):
            hex_display_ratio = 2
            text_display_ratio = 1

        self.horizontal_layout.setStretchFactor(self.hex_display, hex_display_ratio)
        self.horizontal_layout.setStretchFactor(self.text_display, text_display_ratio)




if (__name__ == '__main__'):
    import random
    data = [chr(random.randrange(0,255)) for i in xrange(1200)]
    data = ''.join(data)

    gui = MintGui(data, 0x4030E0, 4, ([0x4030E4, 0x4030E8, 'red'], [0x4032D2, 0x4032D6, 'blue']))
    gui.show()
    #gui.setItemSize(2)
    #gui.setColorsRanges(([0x4030E4, 0x4030E8, 'red'], [0x4032D2, 0x4032D6, 'blue']))

