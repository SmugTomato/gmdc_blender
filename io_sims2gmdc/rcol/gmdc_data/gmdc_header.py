'''
Copyright (C) 2018 SmugTomato

Created by SmugTomato

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


class GMDCHeader:


    def __init__(self, filename, version=4):
        self.version            = version
        self.filename          = filename


    @staticmethod
    def from_data(reader):
        """Build Header from GDMC Data"""
        reader.read_int16()          # Language      0x0001
        reader.read_int16()          # String style  0xFFFF
        reader.read_int32()          # Repeat value  0
        reader.read_int32()          # Index value   1

        # File type     0xAC4F8687
        if not reader.read_uint32() == 0xAC4F8687:
            print("Invalid GMDC File header, [Filetype Failure]")
            return False

        # ‘cGeometryDataContainer’
        try:
            reader.read_byte_string()
        except:
            print("Error reading string value in GMDC Header")
            return False

        # Block ID      0xAC4F8687
        if not reader.read_uint32() == 0xAC4F8687:
            print("Invalid GMDC File header, [BlockID Failure]")
            return False

        # GMDC version  1, 2 or 4
        version  = reader.read_int32()

        # ‘cSGResource’
        try:
            reader.read_byte_string()
        except:
            print("Error reading string value in GMDC Header")
            return False

        # Resource ID and Version: 0, 2
        reader.read_int32()
        reader.read_int32()

        # Internal filename
        try:
            filename = reader.read_byte_string()
        except:
            print("Error reading string value in GMDC Header")
            return False

        return GMDCHeader(filename, version)


    def write(self, writer):
        """Write out the GMDC Header"""
        writer.write_int16( 0x0001 )
        writer.write_int16( 0xFFFF )
        writer.write_int32( 0 )
        writer.write_int32( 1 )
        writer.write_uint32( 0xAC4F8687 )
        writer.write_byte_string( "cGeometryDataContainer" )
        writer.write_uint32( 0xAC4F8687 )
        writer.write_int32( self.version )
        writer.write_byte_string( "cSGResource" )
        writer.write_uint32( 0 )
        writer.write_int32( 2 )
        writer.write_byte_string( self.filename )
