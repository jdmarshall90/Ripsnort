#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import sys
import json
import logging


import apppath


dirname = os.path.dirname(os.path.realpath( __file__ ))

sys.path.append( os.path.join(dirname,"subtitle") )
import caption


class DiscName:
    def __init__(self,disc_name):
        self.originalDiscName = disc_name
        
        title, season, disc = DiscName.titleSeasonAndDiscFromDiscName(DiscName._removeUnnecessaryCharsFromTitle(disc_name))
        self.title = title
        self.season = season
        self.discNumber = disc

        self.formattedName = self.title
        
        if self.season is not None:
            self.formattedName = self.formattedName + ' - Season ' + str(self.season)
        
        if self.discNumber is not None:
            self.formattedName = self.formattedName + ' - DiscNumber ' + str(self.discNumber)
            
        logging.info('DiscName intialized with ' + str(self.title) + ' season ' + str(self.season) + ' discnum ' + str(self.discNumber))

    @staticmethod
    def _removeUnnecessaryCharsFromTitle(title):
        tmpName = title
        
        tmpName = re.sub('(?i)\.iso$', '', tmpName)

        # Clean up
        tmpName = tmpName.replace("\"", "")
        tmpName = tmpName.replace(".", " ")
        tmpName = tmpName.replace("-", " ")
        tmpName = tmpName.replace("  ", " ")

        # Remove anything in brackets
        tmpName = re.sub(r'\[.*?\]','',tmpName)
        tmpName = re.sub(r'\{.*?\}','',tmpName)
        tmpName = re.sub(r'\(\D+\)','',tmpName)
        
        #remove anything in brackets that is not of length 4
        tmpName = re.sub(r'\(\w{5,}?\)','',tmpName)
        tmpName = re.sub(r'\(\w{1,3}?\)','',tmpName)
        
        tmpName = re.sub(r'\-\=.*\=\-','',tmpName)
        tmpName = re.sub(r'\~\=.*\=\~','',tmpName)

        tmpName = re.sub('(?i)\ de\ ', ' the ', tmpName)

        regexRemove = [
                       r'(?i)non[-| ]retail',
                       r'(?i)(?:unrated|extended|special|ultimate|limited|collectors|standard|delux|deluxe|non)?[_| ]?(?:cut|3d|retail|dvd|bluray|blu-ray)?[ |_]?(?:cut|edition|version)',

                       r'(?i)[_| ]?TrueHD7.1',
                       r'(?i)[_| ]?TrueHD5.1',
                       r'(?i)[_| ]?MA[-|_| ]?7.1',
                       r'(?i)[_| ]?MA[-|_| ]?5.1',
                       r'(?i)[_| ]?TrueHD5.1',
                       r'(?i)[_| ]?DTS-MA',
                       r'(?i)[_| ]?DTS-HD',
                       r'(?i)[_| ]?DD-?5.1C?h?',
                       r'(?i)[_| ]?DD-?7.1C?h?',
                       r'(?i)[_| ]?[5|7].1 Audio Channel',
                       r'(?i)[_| ]?[5|7].1 Channel Audio',
                       r'(?i)[_| ]?Dual[\-|\ |\_]?Audio',
                       r'(?i)[_| ]?flac',
                       r'(?i)[_| ]?mp3',
                       r'(?i)[_| ]?aac',
                       r'(?i)[_| ]?aac2',
                       r'(?i)[_| ]?aac3',
                       r'(?i)[_| ]?ac3',

                       r'(?i)[_| ]?srt',
                       r'(?i)[_| ]?vobsub',
                       r'(?i)[_| ]?MSubs',

                       r'(?i)[_| ]?AVC',
                       r'(?i)[_| ]?CHDBits',
                       r'(?i)[_| ]?\[ETRG\]',
                       r'(?i)[_| ]?\[eztv\]',
                       r'(?i)[_| ]?LOL',
                       r'(?i)[_| ]?KILLERS',
                       r'(?i)[_| ]?EVO',
                       r'(?i)[_| ]?RePack?',
                       r'(?i)[_| ]?Codex',
                       r'(?i)[_| ]?YIFY',
                       r'(?i)[_| ]?RARBG',
                       r'(?i)[_| ]?PSYCHD',
                       r'(?i)[_| ]?PublicHD',
                       r'(?i)[_| ]?SPLiTSVILLE',
                       r'(?i)[_| ]?READNFO',
                       r'(?i)[_| ]?\[DE\]',
                       r'(?i)[_| ]?\juggs',
                       r'(?i)[_| ]?\NoGrouP',
                       r'(?i)[_| ]?\SUMO',
                       r'(?i)[_| ]?\MAXSPEED',
                       r'(?i)[_| ]?\New\ Source?',
                       r'(?i)[_| ]?\BiDA',
                       r'(?i)[_| ]?\TeamTNT',
                       r'(?i)[_| ]?\ShAaNiG',
                       r'(?i)[_| ]?2Lions\-Team',
                       r'(?i)[_| ]?padderax',
                       r'(?i)[_| ]?TMRG',
                       r'(?i)[_| ]?MSubs$',
                       r'(?i)[_| ]?D3viL',
                       r'(?i)[_| ]?Mafiaking',
                       r'(?i)[_| ]?Dts-wiki',
                       
                       r'ᴴᴰ',
                       r'(?i)[_| ]?[1|2][_| ]?cd',
                       r'(?i)[_| ]?[1|2][_| ]?dvd',
                       r'(?i)[_| ]?1080p',
                       r'(?i)[_| ]?720p',
                       r'(?i)[_| ]?avi$',
                       r'(?i)[_| ]?xvid',
                       r'(?i)[_| ]?divx',
                       r'(?i)[_| ]?x264',
                       r'(?i)[_| ]?h264',
                       r'(?i)[_| ]?iTunes$',
                       r'(?i)[_| ]?WEB\-?RIP',
                       r'(?i)[_| ]?WEB\-?DL',
                       r'(?i)[_| ]?DVDSCR',
                       r'(?i)[_| ]?HDCAM',
                       r'(?i)[_| ]?HD\-?TS',
                       r'(?i)[_| ]?TS$',
                       r'(?i)[_| ]?hd[\-|\_| ]?rip',
                       r'(?i)[_| ]?br[\-|\_| ]?rip',
                       r'(?i)[_| ]?dvd[\-|\_| ]?rip',
                       r'(?i)[_| ]?pal$',
                       r'(?i)[_| ]?ntsc',
                       r'(?i)[_| ]?dvd$',
                       r'(?i)[_| ]?blu[\-|_| ]?ray',
                       r'(?i)[_| ]?retail',
                       r'(?i)[_| ]?3d']

        didRegexMatch = True
    
        while didRegexMatch:
            didRegexMatch = False

            for regTest in regexRemove:
                matchResults = re.search(regTest,tmpName)
                if matchResults != None:
                    tmpName = re.sub(regTest,'',tmpName)
                    didRegexMatch = True
                    
                    
        tmpName = tmpName.replace('[]','').replace('()','').replace('{}','').replace('--',' ').strip()

        if tmpName[-1] == '-' or tmpName[-1] == '.' or tmpName[-1] == '_' or tmpName[-1] == '\\' or tmpName[-1] == '{' or tmpName[-1] == '}':
            tmpName = tmpName[0:-1]
    
        #capitalize first letter of each word
        tmpName = tmpName.title()
        
        return tmpName.strip()


    @staticmethod
    def titleSeasonAndDiscFromDiscName(disc_name):
        tmpName = disc_name
    
        logging.debug('Removed unnecessary chars to \'' + tmpName + '\'')
    
        #first matching group - season, 2nd - disc number
        regexSeasonDisk = [r'(?i)s([\d{1,2}])_?d([\d{1,2}])',
                           r'(?:season|series)_?([\d{1,2}])_?(?:disc|disk|d)_?([\d{1,2}])',
                           r'(?i)(?:s|series|season)[-|_| ]?([\d{1,2}]).*(?:d|disc|disk)[-|_| ]?([\d{1,2}])',
                           r'(?i)([\d{1,2}])[-|_| ]([\d{1,2}])']

        season = None
        disc = None

        for regTest in regexSeasonDisk:
            regexSearch = re.search(regTest,tmpName)

            if regexSearch != None:
                logging.debug('Matched regex: ' + regTest)
                matchGroups = regexSearch.groups()
                season = int( matchGroups[0] )
                disc = int( matchGroups[1] )
                tmpName = re.sub(regTest,'',tmpName)
                didRegexMatch = True
                
        regexDiskOnly = [r'(?i)(?:d|disc|disk)[-|_| ]?([\b\d{1,2}]\b)']

        for regTest in regexDiskOnly:
            regexSearch = re.search(regTest,tmpName)

            if regexSearch != None:
                logging.debug('Matched regex: ' + regTest)
                matchGroups = regexSearch.groups()
                
                try:
                    disc = int( matchGroups[0] )
                    tmpName = re.sub(regTest,'',tmpName)
                    didRegexMatch = True
                except:
                    pass
            
        #look for numbers prepended to the end of the last word and add space
        numberWhitespacing = r'\b(\D+)(\d+)\b$'
        numberWhitespacingRE = re.compile(numberWhitespacing)
        
        if len(numberWhitespacingRE.findall(tmpName)) > 0:
            whitespaceSearch = numberWhitespacingRE.search(tmpName)
            tmpName = re.sub(numberWhitespacing,whitespaceSearch.groups()[0] + ' ' + whitespaceSearch.groups()[1],tmpName)
            
        tmpName = tmpName.strip()

        #if its a short name, chances are its an acronym i.e CSI
        if len(tmpName) <= 3:
            tmpName = tmpName.upper()
            
        tmpName = re.sub('\s{2,}', ' ', tmpName)

        logging.debug('Converted disc name: \'' +disc_name+ '\' to title:' + tmpName + ', season:' + str(season) + ', disc:' + str(disc))

        return [tmpName,season,disc]


def test():

    assert 'Die Hard' == DiscName._removeUnnecessaryCharsFromTitle('DIE_HARD_PAL')
    assert 'Die Hard' == DiscName._removeUnnecessaryCharsFromTitle('DIE_HARD_NTSC')
    
    expectedText2 = 'Die Hard'
 
    assert expectedText2 == DiscName._removeUnnecessaryCharsFromTitle('Die Hard Limited Edition')
    assert expectedText2 == DiscName._removeUnnecessaryCharsFromTitle('Die Hard limited_Edition')
    assert expectedText2 == DiscName._removeUnnecessaryCharsFromTitle('Die Hard Special Edition')
    assert expectedText2 == DiscName._removeUnnecessaryCharsFromTitle('Die Hard special_edition')
    assert expectedText2 == DiscName._removeUnnecessaryCharsFromTitle('Die Hard Extended Edition')
    assert expectedText2 == DiscName._removeUnnecessaryCharsFromTitle('DIE_HARD_EXTENDED_EDITION')
    assert expectedText2 == DiscName._removeUnnecessaryCharsFromTitle('DIE_HARD_DELUX_VERSION')
    assert expectedText2 == DiscName._removeUnnecessaryCharsFromTitle('DIE HARD DELUXE VERSION')

    assert 'Die Hard' == DiscName._removeUnnecessaryCharsFromTitle('DIE_HARD_SPECIAL_3D_EDITION')
    assert 'Die Hard' == DiscName._removeUnnecessaryCharsFromTitle('DIE_HARD_RETAIL')
    assert 'Die Hard' == DiscName._removeUnnecessaryCharsFromTitle('DIE_HARD_3D_RETAIL')
    assert 'Die Hard' == DiscName._removeUnnecessaryCharsFromTitle('DIE_HARD_DVD')
    assert 'Die Hard' == DiscName._removeUnnecessaryCharsFromTitle('DIE_HARD_BLURAY')
    assert 'Die Hard' == DiscName._removeUnnecessaryCharsFromTitle('DIE_HARD_BLU_RAY')

    assert 'Pals' == DiscName._removeUnnecessaryCharsFromTitle('PALS')
    assert 'Pals' == DiscName._removeUnnecessaryCharsFromTitle('pals')
    
    assert DiscName('band.of.brothers.disc1-padderax').title == 'Band Of Brothers'
    assert DiscName('band.of.brothers.disc1-padderax').discNumber == 1

    assert DiscName('DIE_HARD_SPECIAL_3D_EDITION').title == 'Die Hard'
    assert DiscName('DIE_HARD_SPECIAL_3D_EDITION').season == None
    assert DiscName('DIE_HARD_SPECIAL_3D_EDITION').discNumber == None

    assert DiscName('AVATAR_3D_EDITION').title == 'Avatar'
    assert DiscName('AVATAR_3D_EDITION').season == None
    assert DiscName('AVATAR_3D_EDITION').discNumber == None

    assert DiscName('The Good, the Bad and the Ugly').title == 'The Good, The Bad And The Ugly'
    assert DiscName('The Good, the Bad and the Ugly').season == None
    assert DiscName('The Good, the Bad and the Ugly').discNumber == None

    assert DiscName('CSI2_3').title == 'CSI'
    assert DiscName('CSI2_3').season == 2
    assert DiscName('CSI2_3').discNumber == 3

    assert DiscName('BONES_SEASON_8_F1_DISC_1').title == 'Bones'
    assert DiscName('BONES_SEASON_8_F1_DISC_1').season == 8
    assert DiscName('BONES_SEASON_8_F1_DISC_1').discNumber == 1

    assert DiscName('BONES_SEASON_8_F1_D_1').title == 'Bones'
    assert DiscName('BONES_SEASON_8_F1_D_1').season == 8
    assert DiscName('BONES_SEASON_8_F1_D_1').discNumber == 1

    assert DiscName('BONES_SEASON_8_F1_D1').title == 'Bones'
    assert DiscName('BONES_SEASON_8_F1_D1').season == 8
    assert DiscName('BONES_SEASON_8_F1_D1').discNumber == 1

    assert DiscName('BONES_SEASON_7_DISC_1').title == 'Bones'
    assert DiscName('BONES_SEASON_7_DISC_1').season == 7
    assert DiscName('BONES_SEASON_7_DISC_1').discNumber == 1

    assert DiscName('bones_s7_d1').title == 'Bones'
    assert DiscName('bones_s7_d1').season == 7
    assert DiscName('bones_s7_d1').discNumber == 1

    assert DiscName('bones_season7_d1').title == 'Bones'
    assert DiscName('bones_season7_d1').season == 7
    assert DiscName('bones_season7_d1').discNumber == 1

    assert DiscName('bones_season_7_d1').title == 'Bones'
    assert DiscName('bones_season_7_d1').season == 7
    assert DiscName('bones_season_7_d1').discNumber == 1

    assert DiscName('bones_season_7_d_1').title == 'Bones'
    assert DiscName('bones_season_7_d_1').season == 7
    assert DiscName('bones_season_7_d_1').discNumber == 1
    
    assert DiscName('My.Movie.3D.BluRay.1080p.AVC.TrueHD7.1-CHDBits.iso').title == 'My Movie'
    assert DiscName('My.Movie.2014.3D.BluRay.1080p.AVC.TrueHD7.1-CHDBits.iSo').title == 'My Movie 2014'
    assert DiscName('My.Movie.2014.3D.BluRay.720p.x264.DTS-MA-ac3.ISO').title == 'My Movie 2014'
    
    assert DiscName('My.Movie.2014.3D.BluRay.1080p.AVC.TrueHD7.1-CHDBits.iso').title == 'My Movie 2014'
    
    assert DiscName('red.hood.2010.dvdrip.xvid-qcf').title == 'Red Hood 2010'


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test()
