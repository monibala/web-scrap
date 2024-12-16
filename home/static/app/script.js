<!-- Your custom script -->
<script>
    $(document).ready(function () {
        $("form").submit(function (e) {
            e.preventDefault();
            var query = $("input[name='q']").val();

            $.ajax({
                url: "{% url 'g_scraper' %}",
                method: "GET",
                data: { q: query },
                headers: { "X-Requested-With": "XMLHttpRequest" },
                success: function (response) {
                    console.log("AJAX response:", response);
                    if (response.data) {
                        var data = response.data;
                        var tableBody = $("#scraped-data-table");
                        tableBody.empty();

                        data.forEach(function (item, index) {
                            tableBody.append(
                                "<tr>" +
                                "<td>" + (index + 1) + "</td>" +
                                "<td>" + item.name + "</td>" +
                                "<td>" + item.mobile + "</td>" +
                                "<td>" + item.website + "</td>" +
                                "<td>" + item.address + "</td>" +
                                "</tr>"
                            );
                        });
                    }
                },
                error: function (xhr, status, error) {
                    console.error("AJAX error:", error);
                    console.error("Response:", xhr.responseText);
                }
            });
        });
    });
</script>