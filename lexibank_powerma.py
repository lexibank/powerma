import attr
import lingpy
from pycldf.sources import Source

from pathlib import Path
from clldutils.misc import slug
from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import progressbar

@attr.s
class CustomLanguage(Language):
    SubGroup = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'powerma'
    language_class = CustomLanguage


    def cmd_download(self, args):
        self.raw_dir.download(
                "http://edictor.digling.org/triples/get_data.py?file=signalphabets&remote_dbase=signalphabets",
                'signalphabets.tsv'
                )

    def cmd_makecldf(self, args):
        wl = lingpy.Wordlist(str(self.raw_dir / 'signalphabets.tsv'))

        concepts, sources = {}, {}
        for i, c in enumerate(wl.rows):
            args.writer.add_concept(
                    ID=str(i+1),
                    Name=c,
                    )
            concepts[c] = str(i+1)
        for language in self.languages:
            args.writer.add_language(
                    ID=language['Name_in_Database'],
                    Name=language['Name'],
                        Latitude=language['Latitude'],
                        Longitude=language['Longitude'],
                        Glottocode=language['Glottolog'],
                        SubGroup=language['SubGroup'],
                    )
            sources[language['Name_in_Database']] = language['Source']
        sources['Ukranian_SL'] = 'Lydell2018'
        languages = {language: language for language in sources}
        languages['Ukranian_SL'] = 'Ukrainian_SL'
        
        args.writer.add_sources(*[x for x in self.raw_dir.read_bib() if x.id
            in sources])

        for i, c, l, h1, h2, t, cid in progressbar(wl.iter_rows(
                'concept', 'doculect', 'handshape_1', 
                'handshape_2', 'tokens', 'cogid'), desc='makecldf'):
            row = args.writer.add_form(
                    Value = h1+' '+h2,
                    Language_ID=languages[l],
                    Parameter_ID=concepts[c],
                    Form=t,
                    Source=sources[l]
                    )
            args.writer.add_cognate(
                        lexeme=row,
                        Cognateset_ID=cid,
                        )


