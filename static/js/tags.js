$(function () {
    $(".btn").on("click", function () {
        tag_id = $(this).data('id');
        document.location.href='/articles/tag/' + tag_id;
    });
});