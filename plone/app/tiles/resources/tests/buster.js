var config = module.exports;

var linterConf = {
    linter: 'jshint',
        linterOptions: {
            asi: false,
            bitwise: true,
            boss: false,
            browser: true,
            curly: true,
            devel: false,
            eqeqeq: true,
            evil: false,
            expr: false,
            forin: false,
            immed: true,
            jquery: true,
            latedef: false,
            mootools: false,
            newcap: true,
            node: false,
            noempty: true,
            nomen: false,
            nonew: true,
            onevar: false,
            plusplus: false,
            regexp: false,
            strict: false,
            supernew: true,
            undef: true,
            white: false
        },
        excludes: [
            "jquery"
       ]
};

config.tiles = {
    rootPath: "../",
    environment: "browser",
    libs: [
        "lib/jquery-1.7.2.js"
    ],
    sources: [
        "src/plone.tile.js"
    ],
    tests: [
        "tests/test-tile.js"
    ],
    extensions: [
        require('buster-lint')
    ],
    "buster-lint": linterConf
};
