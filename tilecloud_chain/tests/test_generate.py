# -*- coding: utf-8 -*-

import os
import shutil
from itertools import product

from testfixtures import log_capture
from nose.plugins.attrib import attr

from tilecloud_chain.tests import CompareCase
from tilecloud_chain import generate, controller


class TestGenerate(CompareCase):

    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.dirname(__file__))
        if os.path.exists('/tmp/tiles'):
            shutil.rmtree('/tmp/tiles')

    @classmethod
    def tearDownClass(self):
        os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        if os.path.exists('/tmp/tiles'):
            shutil.rmtree('/tmp/tiles')

    @log_capture('tilecloud_chain', level=30)
    @attr(get_hash=True)
    @attr(general=True)
    def test_get_hash(self, l):
        for d in ('-d', ''):
            self.assert_cmd_equals(
                cmd='./buildout/bin/generate_tiles %s --get-hash 4/0/0 -c tilegeneration/test.yaml -l point' % d,
                main_func=generate.main,
                expected="""Tile: 4/0/0:+8/+8
        empty_metatile_detection:
            size: 20743
            hash: 01062bb3b25dcead792d7824f9a7045f0dd92992
    Tile: 4/0/0
        empty_tile_detection:
            size: 334
            hash: dd6cb45962bccb3ad2450ab07011ef88f766eda8
""")

        l.check()

    @attr(get_wrong_hash=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_get_wrong_hash(self, l):
        for d in ('-d', ''):
            self.assert_cmd_exit_equals(
                cmd='./buildout/bin/generate_tiles %s --get-hash 0/7/5 -c tilegeneration/test.yaml -l all' % d,
                main_func=generate.main,
                expected="""Error: image is not uniform.""")
        l.check()

    @attr(get_bbox=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_get_bbox(self, l):
        for d in ('-d', ''):
            self.assert_cmd_equals(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test.yaml --get-bbox 4/4/4 -l point' % d,
                main_func=generate.main,
                expected="""Tile bounds: [425120,343600,426400,344880]
""")
            self.assert_cmd_equals(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test.yaml --get-bbox 4/4/4:+1/+1 -l point' % d,
                main_func=generate.main,
                expected="""Tile bounds: [425120,343600,426400,344880]
""")
            self.assert_cmd_equals(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test.yaml --get-bbox 4/4/4:+2/+2 -l point' % d,
                main_func=generate.main,
                expected="""Tile bounds: [425120,342320,427680,344880]
""")
        l.check()

    @attr(hash_mapnik=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_hash_mapnik(self, l):
        for d in ('-d', ''):
            self.assert_cmd_equals(
                cmd='./buildout/bin/generate_tiles %s --get-hash 4/0/0 -c tilegeneration/test.yaml -l mapnik' % d,
                main_func=generate.main,
                expected="""Tile: 4/0/0
        empty_tile_detection:
            size: 334
            hash: dd6cb45962bccb3ad2450ab07011ef88f766eda8
""")
        l.check()

    @attr(hash_mapnik_grid=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_hash_mapnik_grid(self, l):
        for d in ('-d', ''):
            self.assert_cmd_equals(
                cmd='./buildout/bin/generate_tiles %s --get-hash 4/0/0 -c tilegeneration/test.yaml -l all' % d,
                main_func=generate.main,
                expected="""Tile: 4/0/0
        empty_tile_detection:
            size: 334
            hash: dd6cb45962bccb3ad2450ab07011ef88f766eda8
""")
        l.check()

    @attr(test_all=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_test_all(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -t 1' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/%s/default/2012/swissgrid_5/%i/%i/%i.png',
                tiles=[
                    ('line', 0, 7, 4), ('polygon', 0, 5, 4)
                ]
            )
        l.check()

    @attr(multigeom=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_multigeom(self, l):
        self.assert_tiles_generated(
            cmd='./buildout/bin/generate_tiles -c tilegeneration/test-multigeom.yaml',
            main_func=generate.main,
            directory="/tmp/tiles/",
            tiles_pattern='1.0.0/pp/default/2012/swissgrid_5/%i/%i/%i.png',
            tiles=[
                (0, 5, 4),
                (0, 5, 5),
                (0, 5, 6),
                (0, 5, 7),
                (0, 6, 4),
                (0, 6, 5),
                (0, 6, 6),
                (0, 6, 7),
                (0, 7, 4),
                (0, 7, 5),
                (0, 7, 6),
                (0, 7, 7),
                (1, 11, 8),
                (1, 11, 9),
                (1, 11, 10),
                (1, 11, 11),
                (1, 11, 12),
                (1, 11, 13),
                (1, 11, 14),
                (1, 12, 8),
                (1, 12, 9),
                (1, 12, 10),
                (1, 12, 11),
                (1, 12, 12),
                (1, 12, 13),
                (1, 12, 14),
                (1, 13, 8),
                (1, 13, 9),
                (1, 13, 10),
                (1, 13, 11),
                (1, 13, 12),
                (1, 13, 13),
                (1, 13, 14),
                (1, 14, 8),
                (1, 14, 9),
                (1, 14, 10),
                (1, 14, 11),
                (1, 14, 12),
                (1, 14, 13),
                (1, 14, 14),
                (1, 15, 8),
                (1, 15, 9),
                (1, 15, 10),
                (1, 15, 11),
                (1, 15, 12),
                (1, 15, 13),
                (1, 15, 14),
                (2, 29, 35),
                (2, 39, 21),
                (3, 78, 42),
                (3, 58, 70),
            ]
        )
        l.check()

    @attr(zoom_identifier=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_zoom_identifier(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -t 1 -l polygon2 -z 0' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/%s/default/2012/swissgrid_01/%s/%i/%i.png',
                tiles=[
                    ('polygon2', '1', 585, 429)
                ]
            )
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -t 1 -l polygon2 -z 1' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/%s/default/2012/swissgrid_01/%s/%i/%i.png',
                tiles=[
                    ('polygon2', '0_2', 2929, 2148)
                ]
            )
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -t 1 -l polygon2 -z 2' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/%s/default/2012/swissgrid_01/%s/%i/%i.png',
                tiles=[
                    ('polygon2', '0_1', 5859, 4296)
                ]
            )
        l.check()

    @attr(serve_kvp=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_serve_kvp(self, l):
        from pyramid.testing import DummyRequest
        from pyramid.httpexceptions import HTTPNoContent, HTTPBadRequest
        from tilecloud_chain.views.serve import Serve

        self.assert_tiles_generated(
            cmd='./buildout/bin/generate_tiles -d -c tilegeneration/test-nosns.yaml '
                '-l point_hash --zoom 1',
            main_func=generate.main,
            directory="/tmp/tiles/",
            tiles_pattern='1.0.0/%s',
            tiles=[
                ('point_hash/default/2012/swissgrid_5/1/11/14.png'),
                ('point_hash/default/2012/swissgrid_5/1/15/8.png'),
            ]
        )
        # use delete to don't delete the repository
        self.assert_tiles_generated_deleted(
            cmd='./buildout/bin/generate_controller --capabilities -c tilegeneration/test-nosns.yaml',
            main_func=controller.main,
            directory="/tmp/tiles/",
            tiles_pattern='1.0.0/%s',
            tiles=[
                ('WMTSCapabilities.xml'),
                ('point_hash/default/2012/swissgrid_5/1/11/14.png'),
                ('point_hash/default/2012/swissgrid_5/1/15/8.png'),
            ]
        )

        request = DummyRequest()
        request.registry.settings = {
            'tilegeneration': {
                'configfile': 'tilegeneration/test-nosns.yaml',
            }
        }
        request.params = {
            'Service': 'WMTS',
            'Version': '1.0.0',
            'Request': 'GetTile',
            'Format': 'png',
            'Layer': 'point_hash',
            'Style': 'default',
            'TileMatrixSet': 'swissgrid_5',
            'TileMatrix': '1',
            'TileRow': '14',
            'TileCol': '11',
        }
        serve = Serve(request)
        serve()
# tilecloud bug
#        self.assertEquals(request.response.content_type, 'image/png')

        request.params['TileRow'] = '15'
        self.assertRaises(HTTPNoContent, serve)

        request.params['Service'] = 'test'
        self.assertRaises(HTTPBadRequest, serve)

        request.params['Service'] = 'WMTS'
        request.params['Request'] = 'test'
        self.assertRaises(HTTPBadRequest, serve)

        request.params['Request'] = 'GetTile'
        request.params['Version'] = '0.9'
        self.assertRaises(HTTPBadRequest, serve)

        request.params['Version'] = '1.0.0'
        request.params['Format'] = 'jpeg'
        self.assertRaises(HTTPBadRequest, serve)

        request.params['Format'] = 'png'
        request.params['Layer'] = 'test'
        self.assertRaises(HTTPBadRequest, serve)

        request.params['Layer'] = 'point_hash'
        request.params['Style'] = 'test'
        self.assertRaises(HTTPBadRequest, serve)

        request.params['Style'] = 'default'
        request.params['TileMatrixSet'] = 'test'
        self.assertRaises(HTTPBadRequest, serve)

        request.params['TileMatrixSet'] = 'swissgrid_5'
        del request.params['Service']
        self.assertRaises(HTTPBadRequest, serve)

        request.params = {
            'Service': 'WMTS',
            'Version': '1.0.0',
            'Request': 'GetCapabilities',
        }
        serve = Serve(request)
        self.assertRaises(HTTPBadRequest, serve)

        l.check()

    @attr(mbtiles_rest=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_mbtile_rest(self, l):
        from pyramid.testing import DummyRequest
        from pyramid.httpexceptions import HTTPNoContent, HTTPBadRequest
        from tilecloud_chain.views.serve import Serve

        self.assert_tiles_generated(
            cmd='./buildout/bin/generate_tiles -d -c tilegeneration/test-nosns.yaml --cache mbtiles'
                ' -l point_hash --zoom 1',
            main_func=generate.main,
            directory="/tmp/tiles/mbtiles/",
            tiles_pattern='1.0.0/%s',
            tiles=[
                ('point_hash/default/2012/swissgrid_5.png.mbtiles')
            ]
        )
        # use delete to don't delete the repository
        self.assert_tiles_generated_deleted(
            cmd='./buildout/bin/generate_controller --capabilities -c tilegeneration/test-nosns.yaml '
                '--cache mbtiles',
            main_func=controller.main,
            directory="/tmp/tiles/mbtiles/",
            tiles_pattern='1.0.0/%s',
            tiles=[
                ('WMTSCapabilities.xml'),
                ('point_hash/default/2012/swissgrid_5.png.mbtiles')
            ]
        )

        request = DummyRequest()
        request.registry.settings = {
            'tilegeneration': {
                'configfile': 'tilegeneration/test.yaml',
                'cache': 'mbtiles',
            }
        }
        request.matchdict = {
            'path': [
                '1.0.0', 'point_hash', 'default', '2012', 'swissgrid_5', '1', '14', '11.png'
            ]
        }
        serve = Serve(request)
        serve()
        self.assertEquals(request.response.content_type, 'image/png')

        request.matchdict['path'][6] = '15'
        self.assertRaises(HTTPNoContent, serve)

        request.matchdict['path'][6] = '14'
        request.matchdict['path'][0] = '0.9'
        self.assertRaises(HTTPBadRequest, serve)

        request.matchdict['path'][0] = '1.0.0'
        request.matchdict['path'][7] = '14.jpeg'
        self.assertRaises(HTTPBadRequest, serve)

        request.matchdict['path'][7] = '14.png'
        request.matchdict['path'][1] = 'test'
        self.assertRaises(HTTPBadRequest, serve)

        request.matchdict['path'][1] = 'point_hash'
        request.matchdict['path'][2] = 'test'
        self.assertRaises(HTTPBadRequest, serve)

        request.matchdict['path'][2] = 'default'
        request.matchdict['path'][4] = 'test'
        self.assertRaises(HTTPBadRequest, serve)

        request.matchdict['path'] = [
            'point_hash', 'default', 'swissgrid_5', '1', '14', '11.png'
        ]
        self.assertRaises(HTTPBadRequest, serve)

        request.matchdict['path'] = [
            '1.0.0', 'WMTSCapabilities.xml'
        ]
        Serve(request)()
        self.assertEquals(request.response.content_type, 'application/xml')
        self.assertEquals(len(request.response.body), 14813)

        l.check()

    @attr(zoom=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_zoom(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l point_hash --zoom 1' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/%s/default/2012/swissgrid_5/%i/%i/%i.png',
                tiles=[
                    ('point_hash', 1, 11, 14), ('point_hash', 1, 15, 8)
                ]
            )
        l.check()

    @attr(zoom_range=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_zoom_range(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l point_hash --zoom 1-3' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/%s/default/2012/swissgrid_5/%i/%i/%i.png',
                tiles=[
                    ('point_hash', 1, 11, 14), ('point_hash', 1, 15, 8),
                    ('point_hash', 2, 29, 35), ('point_hash', 2, 39, 21),
                    ('point_hash', 3, 58, 70), ('point_hash', 3, 78, 42),
                ]
            )
        l.check()

    @attr(no_zoom=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_no_zoom(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l point_hash' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/%s/default/2012/swissgrid_5/%i/%i/%i.png',
                tiles=[
                    ('point_hash', 0, 5, 7), ('point_hash', 0, 7, 4),
                    ('point_hash', 1, 11, 14), ('point_hash', 1, 15, 8),
                    ('point_hash', 2, 29, 35), ('point_hash', 2, 39, 21),
                    ('point_hash', 3, 58, 70), ('point_hash', 3, 78, 42),
                ]
            )
        l.check()

    @attr(py_buffer=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_py_buffer(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml '
                    '-l point_px_buffer --zoom 0-2' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/point_px_buffer/default/2012/swissgrid_5/%i/%i/%i.png',
                tiles=[
                    (0, 5, 7), (0, 7, 4),
                    (1, 11, 14), (1, 15, 8),
                    (2, 29, 35), (2, 39, 21),
                ]
            )
        l.check()

    @attr(zoom_list=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_zoom_list(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l point_hash --zoom 0,2,3' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/%s/default/2012/swissgrid_5/%i/%i/%i.png',
                tiles=[
                    ('point_hash', 0, 5, 7), ('point_hash', 0, 7, 4),
                    ('point_hash', 2, 29, 35), ('point_hash', 2, 39, 21),
                    ('point_hash', 3, 58, 70), ('point_hash', 3, 78, 42),
                ]
            )
        l.check()

    @attr(layer_bbox=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_layer_bbox(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l polygon -z 0' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/polygon/default/2012/swissgrid_5/0/%i/%i.png',
                tiles=list(product((5, 6, 7), (4, 5, 6, 7)))
            )

            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l polygon -z 0'
                ' -b 550000,170000,560000,180000' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/polygon/default/2012/swissgrid_5/0/%i/%i.png',
                tiles=[
                    (6, 5), (7, 5)
                ]
            )

            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l polygon -z 0'
                ' -b 550000.0,170000.0,560000.0,180000.0' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/polygon/default/2012/swissgrid_5/0/%i/%i.png',
                tiles=[
                    (6, 5), (7, 5)
                ]
            )

            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l all -z 0' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/all/default/2012/swissgrid_5/0/%i/%i.png',
                tiles=[
                    (6, 5), (7, 5)
                ]
            )
        l.check()

    @attr(hash_generation=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_hash_generation(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l point_hash -z 0' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/point_hash/default/2012/swissgrid_5/0/%i/%i.png',
                tiles=[
                    (5, 7), (7, 4)
                ]
            )
        l.check()

    @attr(mapnik=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_mapnik(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l mapnik -z 0' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/mapnik/default/2012/swissgrid_5/0/%i/%i.png',
                tiles=list(product((5, 6, 7), (4, 5, 6, 7)))
            )
        l.check()

    @attr(mapnik_grid=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_mapnik_grid(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l mapnik_grid -z 0' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/mapnik_grid/default/2012/swissgrid_5/0/%i/%i.json',
                tiles=list(product((5, 6, 7), (4, 5, 6, 7)))
            )
            f = open('/tmp/tiles/1.0.0/mapnik_grid/default/2012/swissgrid_5/0/5/5.json', 'r')
            self.assert_result_equals(
                f.read(), '{"keys": ["", "1"], "data": {"1": {"name": "polygon1"}}, "grid": '
                '["                ", "                ", "                ", "                ", "                "'
                ', "                ", "                ", "                ", "                ", "                "'
                ', "                ", "                ", "                ", "                ", "!!!!!!!!!!!!!!!!", '
                '"!!!!!!!!!!!!!!!!"]}')
            f = open('/tmp/tiles/1.0.0/mapnik_grid/default/2012/swissgrid_5/0/6/5.json', 'r')
            self.assert_result_equals(
                f.read(), '{"keys": ["1"], "data": {"1": {"name": "polygon1"}}, "grid": '
                '["                ", "                ", "                ", "                ", "                ", '
                '"                ", "                ", "                ", "                ", "                ", '
                '"                ", "                ", "                ", "                ", "                ", '
                '"                "]}')
        l.check()

    @attr(mapnik_grid_drop=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_mapnik_grid_drop(self, l):
        for d in ('-d', ''):
            self.assert_tiles_generated(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l mapnik_grid_drop -z 0' % d,
                main_func=generate.main,
                directory="/tmp/tiles/",
                tiles_pattern='1.0.0/mapnik_grid_drop/default/2012/swissgrid_5/0/%i/%i.json',
                tiles=((5, 7), (7, 4))
            )
        l.check()

    @attr(not_authorised_user=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_not_authorised_user(self, l):
        for d in ('-d', ''):
            self.assert_cmd_exit_equals(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-authorised.yaml' % d,
                main_func=generate.main,
                expected="""not authorised, authorised user is: www-data.""")
        l.check()

    @attr(verbose=True)
    @attr(general=True)
    @log_capture('tilecloud_chain', level=30)
    def test_verbose(self, l):
        for d in ('-d', ''):
            self.run_cmd(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -t 2 -v -l polygon' % d,
                main_func=generate.main
            )
        l.check()

    @attr(time=True)
    @log_capture('tilecloud_chain', level=30)
    def test_time(self, l):
        for d in ('-d', ''):
            self.assert_cmd_equals(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test.yaml --time 2 -l polygon' % d,
                main_func=generate.main,
                expected="""size: 776
size: 860
size: 860
size: 860
time: [0-9]*
size: 860
size: 860
""",
                regex=True,
                empty_err=True)
        l.check()

    @attr(time_layer_bbox=True)
    @log_capture('tilecloud_chain', level=30)
    def test_time_layer_bbox(self, l):
        for d in ('-d', ''):
            self.assert_cmd_equals(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test.yaml --time 2 -l all' % d,
                main_func=generate.main,
                expected="""size: 854
size: 854
size: 854
size: 854
time: [0-9]*
size: 854
size: 854
""",
                regex=True,
                empty_err=True)
        l.check()

#    @attr(daemonize=True)
#    @attr(general=True)
#    @log_capture('tilecloud_chain', level=30)
#    def test_daemonize(self, l):
#        self.assert_cmd_equals(
#            cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test.yaml -t 1 --daemonize' % d,
#            main_func=generate.main,
#            expected="""Daemonize with pid [0-9]*.""",
#            regex=True)
#        l.check()

    def _touch(self, tiles_pattern, tiles):
        for tile in tiles:
            path = tiles_pattern % tile
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            f = open(path, 'w')
            f.close()

    @attr(delete_meta=True)
    @attr(general=True)
    def test_delete_meta(self):
        for d in ('-d', ''):
            if os.path.exists('/tmp/tiles/'):
                shutil.rmtree('/tmp/tiles/')
            self._touch(
                tiles_pattern='/tmp/tiles/1.0.0/point_hash_no_meta/default/2012/swissgrid_5/0/%i/%i.png',
                tiles=list(product(range(12), range(16)))
            )
            self.assert_tiles_generated_deleted(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l point_hash_no_meta -z 0' % d,
                main_func=generate.main,
                directory='/tmp/tiles/',
                tiles_pattern='1.0.0/point_hash_no_meta/default/2012/swissgrid_5/0/%i/%i.png',
                tiles=[
                    (5, 7), (7, 4)
                ]
            )

    @attr(delete_no_meta=True)
    @attr(general=True)
    def test_delete_no_meta(self):
        for d in ('-d', ''):
            if os.path.exists('/tmp/tiles/'):
                shutil.rmtree('/tmp/tiles/')
            self._touch(
                tiles_pattern='/tmp/tiles/1.0.0/point_hash_no_meta/default/2012/swissgrid_5/0/%i/%i.png',
                tiles=list(product(range(12), range(16)))
            )
            self.assert_tiles_generated_deleted(
                cmd='./buildout/bin/generate_tiles %s -c tilegeneration/test-nosns.yaml -l point_hash_no_meta -z 0' % d,
                main_func=generate.main,
                directory='/tmp/tiles/',
                tiles_pattern='1.0.0/point_hash_no_meta/default/2012/swissgrid_5/0/%i/%i.png',
                tiles=[
                    (5, 7), (7, 4)
                ]
            )

    @attr(error_file=True)
    @attr(general=True)
    def test_error_file(self):
        if os.path.exists('error.list'):
            os.remove('error.list')
        self.assert_main_except_equals(
            cmd='./buildout/bin/generate_tiles -c tilegeneration/test-nosns.yaml -l point_error',
            main_func=generate.main,
            expected=[[
                'error.list',
                u"""# \[[0-9][0-9]-[0-9][0-9]-20[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\] Start generation
# \[[0-9][0-9]-[0-9][0-9]-20[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\] Start the layer 'point_error' generation
0/0/0:\+8/\+8 # \[[0-9][0-9]-[0-9][0-9]-20[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\] 'cannot identify image file - .*
0/0/8:\+8/\+8 # \[[0-9][0-9]-[0-9][0-9]-20[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\] 'cannot identify image file - .*
0/8/0:\+8/\+8 # \[[0-9][0-9]-[0-9][0-9]-20[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\] 'cannot identify image file - .*
"""]],
            regex=True)

        self.assert_tiles_generated(
            cmd='./buildout/bin/generate_tiles -d -c tilegeneration/test-nosns.yaml -l point_hash'
                ' --tiles-file error.list',
            main_func=generate.main,
            directory="/tmp/tiles/",
            tiles_pattern='1.0.0/point_hash/default/2012/swissgrid_5/%i/%i/%i.png',
            tiles=[
                (0, 5, 7), (0, 7, 4)
            ]
        )
