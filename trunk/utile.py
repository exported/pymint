

# This library is licensed under GNU Lesser GPL. See the file LICENSE

import struct
from ctypes import *

temp_void_p = c_void_p(1)
temp_void_p.value -= 2
IS_WIN64 = (temp_void_p.value > (2**32))

def DATA( data, base = 0, itemsInRow=0x10 ):
    result = ''
    for i in xrange(0, len(data), itemsInRow):
        line = '%08X  ' % (i + base)
        line_data = data[i:][:itemsInRow]
        for t in xrange(len(line_data)):
            if( (0 == (t % 8)) and (t > 0) ):
                line += '- %02X' % ord(line_data[t])
            elif( 0 == (t & 1) ):
                line += '%02X' % ord(line_data[t])
            elif( 1 == (t & 1) ):
                line += '%02X ' % ord(line_data[t])
            
        spacesLeft = 13 + int(itemsInRow * 2.5) + (2 * ((itemsInRow - 1)//8))
        line += ' ' * (spacesLeft - len(line))
        for t in line_data:
            if( t == `t`[1] ):
                line += t
            else:
                line += '.'
        line += '\n'
        result += line
    return( result )


def makeAddrList( data ):
    if IS_WIN64:
        if len(data) % 8 != 0:
            data += '\x00' * (8 - (len(data) % 8))
        return list(struct.unpack('=' + ('Q' * (len(data) / 8)), data))
    else:
        if len(data) % 4 != 0:
            data += '\x00' * (4 - (len(data) % 4))
        return list(struct.unpack('=' + ('L' * (len(data) / 4)), data))

def makeQwordsList( data ):
    if len(data) % 8 != 0:
        data += '\x00' * (8 - (len(data) % 8))
    return list(struct.unpack('=' + ('Q' * (len(data) / 8)), data))

def makeDwordsList( data ):
    if len(data) % 4 != 0:
        data += '\x00' * (4 - (len(data) % 4))
    return list(struct.unpack('=' + ('L' * (len(data) / 4)), data))

def makeWordsList( data ):
    if len(data) % 2 != 0:
        data += '\x00' * (2 - (len(data) % 2))
    return list(struct.unpack('=' + ('H' * (len(data) / 2)), data))

def makeBytesList( data ):
    return map(ord, data)

def printIntTable( table, base = 0, itemSize=4, itemsInRow = 0x8 ):
    result = ''
    result += ' ' * 17
    itemStr = '%%%dx' % (itemSize * 2)
    for i in range(itemsInRow):
        result += itemStr % (i * itemSize)
        result += ' '
    result += '\n'
    for i in xrange(0, len(table), itemsInRow):
        if 0 == base:
            line = '%16x ' % (i * 4 )
        else:
            line = '%16x ' % ((i * 4) + base)
        line_data = table[i:][:itemsInRow]
        for t in line_data:
            line += itemStr % t
            line += ' '
        spacesLeft = ((itemSize * 2 + 1) * itemsInRow) + 19
        line += ' ' * (spacesLeft - len(line))
        for t in line_data:
            for x in struct.pack('=L', t):
                if( x == `x`[1] ):
                    line += x
                else:
                    line += '.'
        line += '\n'
        result += line
    print result

def printAsQwordsTable( data, base = 0, itemsInRow = 0x8 ):
    table = makeQwordsList(data)
    printIntTable(table, base, itemSize=8, itemsInRow=itemsInRow)
    return table

def printAsDwordsTable( data, base = 0, itemsInRow = 0x8 ):
    table = makeDwordsList(data)
    printIntTable(table, base, itemSize=4, itemsInRow=itemsInRow)
    return table

def printAsWordsTable( data, base = 0, itemsInRow = 0x8 ):
    table = makeWordsList(data)
    printIntTable(table, base, itemSize=2, itemsInRow=itemsInRow)
    return table

def hex2data( h ):
    result = ''
    for i in xrange(0,len(h),2):
        result += chr(int(h[i:i+2],16))
    return result

def data2hex( d ):
    result = ''
    for i in d:
        result += '%02X' % ord(i)
    return result

def hex2dword(x):
    return struct.unpack('=L', hex2data(x))[0]

def readNPrintQwords( self, addr, length = 0x100, isNoBase = True, itemsInRow=4 ):
    if isNoBase:
        printAsQwordsTable(self.readMemory(addr, length), itemsInRow=itemsInRow)
    else:
        printAsQwordsTable(self.readMemory(addr, length), addr, itemsInRow=itemsInRow)

def readNPrintDwords( self, addr, length = 0x100, isNoBase = True, itemsInRow=8 ):
    if isNoBase:
        printAsDwordsTable(self.readMemory(addr, length), itemsInRow=itemsInRow)
    else:
        printAsDwordsTable(self.readMemory(addr, length), addr, itemsInRow=itemsInRow)

def readNPrintWords( self, addr, length = 0x100, isNoBase = True, itemsInRow=0x10 ):
    if isNoBase:
        printAsWordsTable(self.readMemory(addr, length), itemsInRow=itemsInRow)
    else:
        printAsWordsTable(self.readMemory(addr, length), addr, itemsInRow=itemsInRow)

def readNPrintBin( self, addr, length = 0x100, isNoBase = True, itemsInRow=0x10 ):
    if isNoBase:
        print DATA(self.readMemory(addr, length), itemsInRow=itemsInRow)
    else:
        print DATA(self.readMemory(addr, length), addr, itemsInRow=itemsInRow)

def buffDiff( buffers, chunk_size = 1 ):
    if type(buffers) != type([]):
        print 'Invalid type'
        return
    l = len(buffers[0])
    for i in buffers:
        if( type(i) == type([]) ):
            for j in i:
                if( len(j) < l ):
                    l = len(j)
        else:
            if( len(i) < l ):
                l = len(i)
    i = 0
    total_diffs = 0
    while l - i >= chunk_size:
        chunks = []
        diff_this_chunk = True
        for buff in buffers:
            if type(buff) == type([]):
                chunk0 = buff[0][i:i+chunk_size]
                for sub_buff in buff:
                    if sub_buff[i:i+chunk_size] != chunk0:
                        diff_this_chunk = False
                        break
                if False == diff_this_chunk:
                    break
                else:
                    chunks.append(chunk0[:])
            else:
                chunks.append( buff[i:i+chunk_size] )

        if True == diff_this_chunk:
            #chunks = map(lambda x:x[i:i+chunk_size], buffers)
            chunk0 = chunks[0]
            for chunk in chunks:
                if chunk != chunk0:
                    if( 1 == chunk_size ):
                        print "Buff diff at %04X: " % (i),
                        for chunk in chunks:
                            print "%02X " % ord(chunk),
                        print
                    elif( 2 == chunk_size ):
                        print "Buff diff at %04X: " % (i),
                        for chunk in chunks:
                            print "%04X " % (struct.unpack('=H',chunk)[0]),
                        print
                    elif( 4 == chunk_size ):
                        print "Buff diff at %04X: " % (i),
                        for chunk in chunks:
                            print "%08X " % (struct.unpack('=L',chunk)[0]),
                        print
                    else:
                        print "Buff diff at %04X: " % (i)
                        for chunk in chunks:
                            print "\t%s" % data2hex(chunk)
                    total_diffs += 1
                    break
        i += chunk_size
    if( 0 == total_diffs ):
        print "Buffers match!"
    else:
        print "Total diffs %d" % total_diffs

###def printf( debug_context, stack_address ):
### formated_string = debug_context.readString( debug_context.readDword(stack_address) )
### result = ''
### pos = 0
### while pos < len(formated_string):
###     char = formated_string[pos]
###     if '\\' == char:
###         next_char = formated_string[pos+1]
###         if '\\' == next_char:
###             result += '\\'
###             pos += 1
###         elif '%' == next_char:
###             result += '%'
###             pos += 1
###     if '%' == char:
###         next_char = 
###         while 
###         if formated_string
###     pos += 1

def dotted(ip):
    result = '%d.%d.%d.%d' % ((ip >> 24) & 0xff, (ip >> 16) & 0xff, (ip >> 8) & 0xff, ip & 0xff)
    return result


try:
    isTkFound = True
    from Tkinter import *
    import thread
    import time
except ImportError, e:
    # No Tkinter module
    isTkFound = False

if isTkFound:
    class DisplayContext( object ):
        def __init__(self, data, addr = 0, isNoBase = True):
            self.data = data
            self.addr = addr
            length = len(data)
            self.length = length
            self.isNoBase = isNoBase
            self.colors = {}
            root = Tk()
            root.title("Memory @ 0x%08x length: 0x%x" % (addr, length))
            scrollbar = Scrollbar(root)
            address = Text(root, yscrollcommand=scrollbar.set)
            hexBytes = Text(root, yscrollcommand=scrollbar.set)
            asciiBytes = Text(root, yscrollcommand=scrollbar.set)
            address.config(width=9, height = 20)
            hexBytes.config(width=40, height = 20)
            asciiBytes.config(width=16, height = 20)
            scrollbar.pack(side=RIGHT, fill=Y)
            textBoxes = [address, hexBytes, asciiBytes]
            for textBox in textBoxes:
                textBox.config(font=('Terminal', 10, 'normal'))
                textBox.pack(expand=YES, side=LEFT, fill=Y)
            def scrollAllThree( cmd,offset ):
                    address.yview(cmd, offset)
                    hexBytes.yview(cmd, offset)
                    asciiBytes.yview(cmd, offset)
            scrollbar.config(command=scrollAllThree)
            root.resizable(NO, YES)
            address.focus_set()
            # Create thread to handle the window's events
            thread.start_new_thread(mainloop, ())
            time.sleep(0.2)
            # Add the data in
            for pos in xrange(0, length, 0x10):
                address.insert(END, '%08X' % (addr + pos))
                for i in xrange(0x10):
                    if (pos + i) < length:
                        if 1 == (i % 2):
                            hexBytes.insert(END, "%02x " % ord(data[pos+i]))
                        else:
                            hexBytes.insert(END, "%02x" % ord(data[pos+i]))
                        if `data[pos+i]`[1] == data[pos+i]:
                            asciiBytes.insert(END, data[pos+i])
                        else:
                            asciiBytes.insert(END, '.')
                address.insert(END, '\n')
                hexBytes.insert(END, '\n')
                asciiBytes.insert(END, '\n')
            # Don't let the user change the text
            for textBox in textBoxes:
                textBox.config(state = DISABLED)
            # Save everything to context
            self.root = root
            self.address = address
            self.hexBytes = hexBytes
            self.asciiBytes = asciiBytes
            self.scrollbar = scrollbar
        def setByteColor(self, addr, length, color):
            if length < 1:
                return
                #raise Exception("Invalid length")
            if (addr < self.addr) or ((addr + length) > (self.addr + self.length)):
                return
                #raise Exception("Invalid address")
            offset = addr - self.addr
            endOffset = addr + length - self.addr
            lineNumber = (offset / 0x10) + 1
            endLineNumber = (endOffset / 0x10) + 1
            rowNumber = offset % 0x10
            rowEndNumber = endOffset % 0x10
            if color not in self.colors:
                colorId = 'color%04x' % len(self.colors)
                self.colors[color] = colorId
                self.address.tag_config(colorId, background=color)
                self.hexBytes.tag_config(colorId, background=color)
                self.asciiBytes.tag_config(colorId, background=color)
            else:
                colorId = self.colors[color]
            if 0 != rowEndNumber:
                self.address.tag_add(colorId, '%d.0' % lineNumber, '%d.8' % endLineNumber)
            else:
                self.address.tag_add(colorId, '%d.0' % lineNumber, '%d.8' % (endLineNumber - 1))
            self.hexBytes.tag_add(colorId, 
                    '%d.%d' % (lineNumber, rowNumber * 2 + (rowNumber / 2)),
                    '%d.%d' % (endLineNumber, rowEndNumber * 2 + ((rowEndNumber-1) / 2)))
            self.asciiBytes.tag_add(colorId, '%d.%d' % (lineNumber, rowNumber), '%d.%d' % (endLineNumber, rowEndNumber))

    def windowDisplay( self, addr, length = 0x100, isNoBase = True ):
        data = self.readMemory(addr, length)
        dc = DisplayContext( data, addr, isNoBase )
        return dc


else:
    windowDisplay = None
    setByteColor = None

