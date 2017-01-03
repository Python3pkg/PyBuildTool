# where `waf` will store its configuration
top = '.'
# directory for temporary files created during build process
out = '.BUILD'

# Constants

# stages, for example: 'dev' will provide separate build environment with
# commands like `waf build_dev` and `waf clean_dev`, that is build variants
STAGES = ('dev', 'stage', 'prod')


def build(bld):
    # load main configuration file
    import os, yaml
    from pybuildtool.misc.resource import prepare_targets
    from pybuildtool.misc.yaml import OrderedDictYAMLLoader
    conf_file = os.path.join(bld.path.abspath(), 'build_rules.yml')
    with open(conf_file) as f:
        conf = yaml.load(f, Loader=OrderedDictYAMLLoader)
    # parse data as waf tasks
    prepare_targets(conf, bld)


def options(opt):
    import os
    # add loadable modules from waf root directory
    import sys
    sys.path.append(opt.path.abspath())
    # load predefined tools from pybuildtool
    from imp import find_module
    pybuildtool_dir = find_module('pybuildtool')[1]
    addons_dir = os.path.join(pybuildtool_dir, 'addons')
    opt.load('watch', tooldir=addons_dir)


def configure(ctx):
    import os
    # load predefined tools from pybuildtool
    from imp import find_module
    pybuildtool_dir = find_module('pybuildtool')[1]
    tools_dir = os.path.join(pybuildtool_dir, 'tools')
    #ctx.load('autoprefixer', tooldir=tools_dir)
    #ctx.load('browserify', tooldir=tools_dir)
    #ctx.load('cleancss', tooldir=tools_dir)
    #ctx.load('concat', tooldir=tools_dir)
    #ctx.load('cp', tooldir=tools_dir)
    #ctx.load('gzip', tooldir=tools_dir)
    #ctx.load('handlebars', tooldir=tools_dir)
    #ctx.load('html_lint', tooldir=tools_dir)
    #ctx.load('jinja', tooldir=tools_dir)
    #ctx.load('jshint', tooldir=tools_dir)
    #ctx.load('lesscss', tooldir=tools_dir)
    #ctx.load('lftp', tooldir=tools_dir)
    #ctx.load('nunjucks', tooldir=tools_dir)
    #ctx.load('patch', tooldir=tools_dir)
    #ctx.load('pngcrush', tooldir=tools_dir)
    #ctx.load('pylint', tooldir=tools_dir)
    #ctx.load('rjs', tooldir=tools_dir)
    #ctx.load('scp', tooldir=tools_dir)
    #ctx.load('shell', tooldir=tools_dir)
    #ctx.load('stylus', tooldir=tools_dir)
    #ctx.load('ttf2eot', tooldir=tools_dir)
    #ctx.load('ttf2svg', tooldir=tools_dir)
    #ctx.load('ttf2woff', tooldir=tools_dir)
    #ctx.load('uglifyjs', tooldir=tools_dir)


from waflib.Build import BuildContext, CleanContext, InstallContext
from waflib.Build import UninstallContext
from waflib.Context import Context

class WatchContext(Context):
    cmd = 'watch'
    fun = 'watch'
    variant = STAGES[0]

for stage in STAGES:
    for build_class in (BuildContext, CleanContext, InstallContext,
            UninstallContext, WatchContext):
        name = build_class.__name__.replace('Context', '').lower()
        class TempClass(build_class):
            cmd = name + '_' + stage
            variant = stage
