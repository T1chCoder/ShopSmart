$(document).ready(function () {
    $("html").click(function () {
        $(".html-close-js").removeAttr("style");
        $(".html-remove-js").remove();
    });

    $("html").on("click", ".stop-prop", function (e) {
        e.stopPropagation();
    });

    $("html").on("click", ".submit-form", function () {
        $("#" + $(this).attr("form")).submit();
    });

    $("html").on("click", ".submit-form-act", function () {
        var url = $(this).attr("formurl");
        var form = $("#" + $(this).attr("form"));
        form.prop("action", url);
        form.submit();
    });

    $("html").on("click", ".click-another-block", function (e) {
        $("." + $(this).attr("blockClass")).click();
    });
});