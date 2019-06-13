# coding=utf-8
from __future__ import unicode_literals, print_function

import attr
import lingpy
from pycldf.sources import Source

from clldutils.path import Path
from clldutils.misc import slug
from pylexibank.dataset import Metadata, Concept, Language
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb, get_url, textdump
import json
from urllib import request


#@attr.s
#class OurConcept(Concept):
#    TBL_ID = attr.ib(default=None)
#    Coverage = attr.ib(default=None)
#
#@attr.s
#class OurLanguage(Language):
#    Name_in_Text = attr.ib(default=None)
#    Name_in_Source = attr.ib(default=None)
#    Subgroup = attr.ib(default=None)
#    Coverage = attr.ib(default=None)
#    Longitude = attr.ib(default=None)
#    Latitude = attr.ib(default=None)
#    Source = attr.ib(default=None)

    

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'powerma'


    def cmd_download(self, **kw):
        self.raw.download(
                "http://edictor.digling.org/triples/get_data.py?file=signalphabets&remote_dbase=signalphabets",
                'signalphabets.tsv'
                )

    def cmd_install(self, **kw):
        wl = lingpy.Wordlist(self.raw.posix('signalphabets.tsv'))

        with self.cldf as ds:
            cids, lids = {}, {}
            for i, c in enumerate(wl.rows):
                ds.add_concept(
                        ID=str(i+1),
                        Name=c
                        )
                cids[c] = str(i+1)
            for i, l in enumerate(wl.cols):
                ds.add_language(
                        ID=str(i+1),
                        Name=l
                        )
                lids[l] = str(i+1)

            for i, c, l, h1, h2, t, cid in pb(wl.iter_rows(
                    'concept', 'doculect', 'handshape_1', 
                    'handshape_2', 'tokens', 'cogid')):
                for row in ds.add_lexemes(
                        Value = h1+' '+h2,
                        Language_ID=lids.get(l, l),
                        Parameter_ID=cids.get(c, c),
                        Form=t,
                        Cognacy=cid
                        ):
                    ds.add_cognate(
                            lexeme=row,
                            Cognateset_ID=cid,
                            )


