$(document).ready(function () {
    function showCompanyInfo() {
        $('#account-info').hide();
        $('#company-info').show();
        $('.step.company-info').addClass('active');
        $('.step.account-info').removeClass('active');
    };

    function showAccountInfo() {
        $('#company-info').hide();
        $('#account-info').show();
        $('.step.company-info').removeClass('active');
        $('.step.account-info').addClass('active');
    };

    $('.step.company-info').click(() => showCompanyInfo());
    $('.step.account-info').click(() => showAccountInfo());
    $('.sign-up-back').click(() => showAccountInfo());
    $('.sign-up-next').click(() => showCompanyInfo());

});
