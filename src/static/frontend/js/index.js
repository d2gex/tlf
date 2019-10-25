$(document).ready(function () {

    var jsonStr = $("pre").text();
    var jsonObj = JSON.parse(jsonStr);
    var jsonPretty = JSON.stringify(jsonObj, null, 4);
    $("pre").text(jsonPretty);
});