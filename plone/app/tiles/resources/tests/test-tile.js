/*global refute: false, document:false, $: false, buster:false, assert: false */
"use strict";

buster.testCase("Namespaces", {
    'plone namespace exists': function () {
        assert.defined($.plone);
    },

    'tile namespace exists': function () {
        assert.defined($.plone.tile);
    }
});

buster.testCase("Tile", {

    setUp: function() {
        var self = this;
        $(document.body).html('<div id="tile"/>');
        $.deco = $.deco || {};
        $.fn.ploneOverlay = self.stub();
        $.plone.tiletype = $.plone.tiletype || {};
        $.plone.tiletype.get = function () {
            return function () {
                return {'getActions': self.stub().returns('actions')};
            };
        };
        $.plone.tiletype.getTileNameByElement = $.plone.tiletype.getTileNameByElement || function () {
            return function () {};
        };
        $.plone.tiletype.getActions = this.stub();
        $.fn.ploneTile = $.fn.ploneTile || this.spy();
    },

    tearDown: function() {
        $('#tile').remove();
    },

    'Initialize type': function () {
        var tile = new $.plone.tile.Tile($('#tile'));
        assert.isObject(tile.type);
    },

    'Initialize actions': function () {
        var tile = new $.plone.tile.Tile($('#tile'));
        assert.equals(tile.actions, 'actions');
    },

    'Initialize element': function () {
        var tile = new $.plone.tile.Tile($('#tile'));
        assert.equals(tile.el, $('#tile'));
    },

    'Initialize wrapper': function () {
        var tile = new $.plone.tile.Tile($('#tile'), {'wrapper': 'wrapper'});
        assert.equals(tile.wrapper, 'wrapper');
    },

    'Initialize option': function () {
        var tile = new $.plone.tile.Tile($('#tile'), {'option1': 'option1'});
        assert.equals(tile.options.option1, 'option1');
    },

    'Initialize overlay': function () {
        var tile = new $.plone.tile.Tile($('#tile'), {'overlay': 'overlay'});
        assert.equals(tile.options.overlay, 'overlay');
    },

    'Undefined wrapper': function () {
        var tile = new $.plone.tile.Tile($('#tile'));
        refute.defined(tile.wrapper);
    }

});

buster.testCase('Show', {

    setUp: function() {
        var self = this;
        $(document.head).html('<base href="http://nohost/plone/" /> ');
        $(document.body).html('<div id="tile" data-tile="@@my.tile/12345">foo</div>');
        $.deco = $.deco || {};
        $.fn.ploneOverlay = self.stub();
        $.plone.tiletype = $.plone.tiletype || {};
        $.plone.tiletype.get = function () {
            return function () {
                return {'name': 'tile-name', 'getActions': self.stub().returns($('<div class="actions"><ul><li><a class="plone-tiletype-action-edit">edit</a></li><li><a class="plone-tiletype-action-remove">remove</a></li></ul></div'))};
            };
        };
        $.plone.tiletype.getTileNameByElement = $.plone.tiletype.getTileNameByElement || function () {
            return function () {};
        };
        $.plone.tiletype.getActions = this.stub();
        $.fn.ploneTile = $.fn.ploneTile || this.spy();
    },

    tearDown: function() {
        $('#tile').remove();
    },

    'Show Tile': function () {
        var tile = new $.plone.tile.Tile($('#tile'));
        tile.show();
        assert(tile.wrapper.hasClass('plone-tile'));
        assert.equals(tile.wrapper.find('#tile').length, 1);
        assert.equals(tile.wrapper.css('position'), 'relative');
        assert.equals(tile.wrapper.find('.actions').length, 1);
    },

    'Hover when visible': function () {
        var tile = new $.plone.tile.Tile($('#tile'));
        tile.show();
        assert(tile.actions.is(':visible'));
        $('.plone-tiletype-action-edit').trigger('mouseout');
        refute(tile.actions.is(':visible'));
    },

    'Hover when hidden': function () {
        var tile = new $.plone.tile.Tile($('#tile'));
        tile.show();
        tile.actions.hide();
        refute(tile.actions.is(':visible'));
        $('.plone-tiletype-action-edit').trigger('mouseover');
        assert(tile.actions.is(':visible'));
    },

    'Hover wrapper when visible': function () {
        var tile = new $.plone.tile.Tile($('#tile'));
        tile.show();
        assert(tile.actions.is(':visible'));
        $('.plone-tile').trigger('mouseover');
        refute(tile.actions.is(':visible'));
    },

    'Hover wrapper when hidden': function () {
        var tile = new $.plone.tile.Tile($('#tile'));
        tile.show();
        tile.actions.hide();
        refute(tile.actions.is(':visible'));
        $('.plone-tile').trigger('mouseout');
        assert(tile.actions.is(':visible'));
    },

    //'Edit action': function () {
    //    var tile = new $.plone.tile.Tile($('#tile'));
    //    tile.show();
    //    assert.equals(
    //        $('.plone-tiletype-action-edit').attr('href'),
    //        'http://nohost/plone/@@edit-tile/tile-name/12345'
    //        );
    //},

    //'Remove action': function () {
    //    var tile = new $.plone.tile.Tile($('#tile'));
    //    tile.show();
    //    $('.plone-tiletype-action-remove').click();
    //}

});
