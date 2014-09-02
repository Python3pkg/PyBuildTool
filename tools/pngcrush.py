"""
pngcrush is a png compressor

Options:

    * already       : int,   None,  already_crushed_size [e.g., 8192]
    * bail          : bool,  False, bail out of trial when size exceeds best size
                      found
    * bit_depth     : int,   None,  bit depth to use in output file
    * blacken       : bool,  False, zero samples underlying fully-transparent pixels
    * brute         : int,   148,   use brute-force: try 138 different methods [11-148]
    * color_type    : int,   None,  color_type of output file [0, 2, 4, or 6]
    * double_gamma  : bool,  False, used for fixing gamma in PhotoShop 5.0/5.02 files
    * extension     : str,   None,  used for creating output filename
    * filter        : int,   None,  user_filter [0-5] for specified method
    * fix           : bool,  True,  fix otherwise fatal conditions such as bad CRCs
    * force         : bool,  False, write a new output file even if larger than input
    * gamma         : float, None,  gamma (float or fixed*100000, e.g., 0.45455 or 45455)
    * huffman       : bool,  False, use only zlib strategy 2, Huffman-only
    * iccp          : int,   None,  length "Profile Name" iccp_file
    * itxt          : str,   None,  b[efore_IDAT]|a[fter_IDAT] "keyword"
    * keep          : bool,  False, chunk_name
    * level         : int,   None,  zlib_compression_level [0-9] for specified method
    * loco          : bool,  False, "loco crush" truecolor PNGs
    * method        : int,   None,  method [1 through 200]
    * max           : int,   None,  maximum_IDAT_size [default 8192]
    * mng           : bool,  False, write a new MNG, do not crush embedded PNGs
    * nobail        : bool,  False, do not bail out early from trial -- see "-bail"
    * nofilecheck   : bool,  False, do not check for infile.png == outfile.png
    * nolimits      : bool,  False, turns off limits on width, height, cache, malloc
    * noreduce      : bool,  False, turns off "-reduce" operations
    * oldtimestamp  : bool,  False, do not reset file modification time
    * overwrite     : bool,  True,  overwrite
    * reduce        : bool,  False, do lossless color-type or bit-depth reduction
    * rem           : bool,  False, chunkname (or "alla" or "allb")
    * replace_gamma : float, None,  gamma (float or fixed*100000) even if it is present
    * resolution    : int,   None,  resolution in dpi
    * rle           : bool,  False, use only zlib strategy 3, RLE-only
    * save          : bool,  False, keep all copy-unsafe PNG chunks
    * srgb          : int,   None,  [0, 1, 2, or 3]
    * ster          : int,   None,  [0 or 1]
    * text          : str,   None,  b[efore_IDAT]|a[fter_IDAT] "keyword" "text"
    * trns_array    : str,   None,  n trns[0] trns[1] .. trns[n-1]
    * trns          : str,   None,  index red green blue gray
    * window_size   : int,   None,  compression_window_size [32, 16, 8, 4, 2, 1, 512]
    * zlib          : int,   None,  zlib_strategy [0, 1, 2, or 3] for specified method
    * zmem          : int,   None,  zlib_compression_mem_level [1-9, default 9]
    * zitxt         : str,   None,  b|a "keyword" "lcode" "tkey" "text"
    * ztxt          : str,   None,  b[efore_IDAT]|a[fter_IDAT] "keywrod" "text"

Requirements:

    * pngcrush
      make available from executable $PATH
"""

from PyBuildTool.utils.common import (
    perform_shadow_jutsu,
    finalize_shadow_jutsu,
    silent_str_function,
)
from PyBuildTool.utils.warnings import ThereCanBeOnlyOne
from SCons.Action import Action
from SCons.Builder import Builder
from SCons.Errors import StopError
from SCons.Node.Python import Value

tool_name = 'pngcrush'
file_processor = 'pngcrush'

def tool_str(target, source, env):
    perform_shadow_jutsu(target=target, source=source, env=env)
    return env.subst('%s compressed $TARGETS.attributes.RealName' % tool_name,
                     target=target)

def tool_generator(source, target, env, for_signature):
    perform_shadow_jutsu(target=target, source=source, env=env)

    src = [s.attributes.RealName for s in source if s.attributes.RealName]
    tgt = [t.attributes.RealName for t in target if t.attributes.RealName]

    if len(src) != 1:
        raise StopError(ThereCanBeOnlyOne,
                        '%s only take one source' % tool_name)
    if len(tgt) != 1:
        raise StopError(ThereCanBeOnlyOne,
                        '%s only build one target' % tool_name)

    env['%s_BIN' % tool_name.upper()] = file_processor

    args = []
    cfg = env.get('TOOLCFG', {})
    if isinstance(cfg, Value):  cfg = cfg.read()

    # already_crushed_size [e.g., 8192]
    if cfg.get('already', None):
        args.append('-already %i' % cfg['already'])

    # bail out of trial when size exceeds best size found
    if cfg.get('bail', False):
        args.append('-bail')

    # bit depth to use in output file
    if cfg.get('bit_depth', None):
        args.append('-bit_depth %s' % cfg['bit_depth'])

    # zero samples underlying fully-transparent pixels
    if cfg.get('blacken', False):
        args.append('-blacken')

    # use brute-force: try 138 different methods [11-148]
    args.append('-brute %i' % cfg.get('brute', 148))

    # color_type of output file [0, 2, 4, or 6]
    if cfg.get('color_type', None):
        args.append('-c %i' % cfg['color_type'])

    # used for fixing gamma in PhotoShop 5.0/5.02 files
    if cfg.get('double_gamma', False):
        args.append('-double_gamma')

    # used for creating output filename
    if cfg.get('extension', None):
        args.append('-e %s' % cfg['extension'])

    # user_filter [0-5] for specified method
    if cfg.get('filter', None):
        args.append('-f %i' % cfg['filter'])
    
    # fix otherwise fatal conditions such as bad CRCs
    if cfg.get('fix', True):
        args.append('-fix')
    
    # write a new output file even if larger than input
    if cfg.get('force', None):
        args.append('-force')

    # gamma (float or fixed*100000, e.g., 0.45455 or 45455)
    if cfg.get('gamma', None):
        args.append('-g %s' % cfg['gamma'])

    # use only zlib strategy 2, Huffman-only
    if cfg.get('huffman', False):
        args.append('-huffman')

    # length "Profile Name" iccp_file
    if cfg.get('iccp', None):
        args.append('-iccp %i' % cfg['iccp'])

    # b[efore_IDAT]|a[fter_IDAT] "keyword"
    if cfg.get('itxt', None):
        args.append('-itxt %s' % cfg['itxt'])

    # chunk_name
    if cfg.get('keep', False):
        args.append('-keep')

    # zlib_compression_level [0-9] for specified method
    if cfg.get('level', None):
        args.append('-l %i' % cfg['level'])

    # "loco crush" truecolor PNGs
    if cfg.get('loco', False):
        args.append('-loco')

    # method [1 through 200]
    if cfg.get('method', None):
        args.append('-m %i' % cfg['method'])

    # maximum_IDAT_size [default 8192]
    if cfg.get('max', None):
        args.append('-max %i' % cfg['max'])

    # write a new MNG, do not crush embedded PNGs
    if cfg.get('mng', False):
        args.append('-mng')

    # do not bail out early from trial -- see "-bail"
    if cfg.get('nobail', None):
        args.append('-nobail')

    # do not check for infile.png == outfile.png
    if cfg.get('nofilecheck', False):
        args.append('-nofilecheck')

    # turns off limits on width, height, cache, malloc
    if cfg.get('nolimits', False):
        args.append('-nolimits')

    # turns off "-reduce" operations
    if cfg.get('noreduce', False):
        args.append('-noreduce')

    # do not reset file modification time
    if cfg.get('oldtimestamp', False):
        args.append('-oldtimestamp')

    # overwrite
    if cfg.get('overwrite', True):
        args.append('-ow')

    # do lossless color-type or bit-depth reduction
    if cfg.get('reduce', True):
        args.append('-reduce')

    # chunkname (or "alla" or "allb")
    if cfg.get('rem', None):
        args.append('-rem %s' % cfg['rem'])

    # gamma (float or fixed*100000) even if it is present
    if cfg.get('replace_gamma', None):
        args.append('-replace_gamma %s' % cfg['replace_gamma'])

    # resolution in dpi
    if cfg.get('resolution', None):
        args.append('-res %i' % cfg['resolution'])

    # use only zlib strategy 3, RLE-only
    if cfg.get('rle', False):
        args.append('-rle')

    # keep all copy-unsafe PNG chunks
    if cfg.get('save', False):
        args.append('-save')

    # srgb
    if cfg.get('srgb', None):
        args.append('-srgb %i' % cfg['srgb'])

    # ster
    if cfg.get('ster', None):
        args.append('-ster %i' % cfg['ster'])

    # b[efore_IDAT]|a[fter_IDAT] "keyword" "text"
    if cfg.get('text', None):
        args.append('-text %s' % cfg['text'])

    # trns_array: n trns[0] trns[1] .. trns[n-1]
    if cfg.get('trns_array', None):
        args.append('-trns_array %s' % cfg['trns_array'])

    # index red green blue gray
    if cfg.get('trns', None):
        args.append('-trns %s' % cfg['trns'])

    # compression_window_size [32, 16, 8, 4, 2, 1, 512]
    if cfg.get('window_size', None):
        args.append('-w %i' % cfg['window_size'])

    # zlib_strategy [0, 1, 2, or 3] for specified method
    if cfg.get('zlib', None):
        args.append('-z %i' % cfg['zlib'])

    # zlib_compression_mem_level [1-9, default 9]
    if cfg.get('zmem', None):
        args.append('-zmem %i' % cfg['zmem'])

    # b|a "keyword" "lcode" "tkey" "text"
    if cfg.get('zitxt', None):
        args.append('-zitxt %s' % cfg['zitxt'])

    # b[efore_IDAT]|a[fter_IDAT] "keywrod" "text"
    if cfg.get('ztxt', None):
        args.append('-ztxt %s' % cfg['ztxt'])

    env['%s_ARGS' % tool_name.upper()] = ' '.join(args)

    return [
        Action(finalize_shadow_jutsu, silent_str_function),
        Action(
            '${t}_BIN ${t}_ARGS $SOURCES.attributes.RealName '
            '-o $TARGETS.attributes.RealName'.format(t=tool_name.upper()),
            tool_str,
        ),
    ]

def generate(env):
    """Add builders and construction variables to the Environment."""

    env['BUILDERS'][tool_name] = Builder(generator=tool_generator)

def exists(env):
    return env.Detect(file_processor)
