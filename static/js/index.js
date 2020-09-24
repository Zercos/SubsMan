import './semantic.min.js'

$(document).ready(function () {
    // adds CSRF token header to ajax requests to avoid "Can't verify CSRF token authenticity" error
    $.ajaxPrefilter(function (options) {
        if (!options.beforeSend) {
            options.beforeSend = function (xhr) {
                xhr.setRequestHeader('X-CSRF-Token', $('meta[name="csrf-token"]').attr('content'));
            }
        }
    });

    $(window).resize(function () {
        if ($(window).width() >= 992) {
            $('.ui.left.sidebar').sidebar('show');
            $('#sidebar-toggle').hide();
        } else {
            $('.ui.left.sidebar').sidebar('hide');
            $('#sidebar-toggle').show();
        }
    }).resize();

    $('.ui.left.sidebar').sidebar({
        dimPage: false,
        transition: 'push',
        exclusive: false,
        closable: false
    });

    if ($('#sidebar-toggle').length) { // sidebar is present only for logged-in user
        $('.ui.left.sidebar').sidebar('attach events', '#sidebar-toggle');
    }

    $('.ui.dropdown').dropdown();

    // basket icon on top menu
    $('.basket-open').click(() => {
        $('.basket-container').slideToggle();
    });

    $('.basket-close').click(() => {
        $('.basket-container').slideUp();
    });

    if ($('body').is('.subscriptions.create,.subscriptions.new,.users.new_subscription')) {
        $('.basket-container').show();
        $('.basket-close').hide();
        $('.basket-checkout').hide();
        $('.basket-delete').hide();
    } else {
        $('.basket-container').hide();
        $('.basket-close').show();
        $('.basket-checkout').show();
        $('.basket-delete').show();
    }

    $('.basket-delete').click(() => {
        document.cookie = 'lc_basket=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        location.reload();
    });

    // trigger add-card form
    $('.add-card').click(() => {
        $('.stripe-button-el').trigger('click');
    });
});
