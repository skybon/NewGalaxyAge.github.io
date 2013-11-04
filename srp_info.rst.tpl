.. Файл srp_info.rst автоматически генерируется из файла srp_info.rst.tpl

.. raw:: html

    <script src="http://cdnjs.cloudflare.com/ajax/libs/flot/0.8.1/jquery.flot.min.js"></script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/flot/0.8.1/jquery.flot.time.min.js"></script>

    <script>
    $(function() {{
      $.getJSON('srp.json', function(data) {{
        $.plot(
          $('<div>')
            .css('width', '800px')
            .css('height', '300px')
            .insertBefore($('#raisa-srp table')),
          [data],
          {{
            xaxis: {{mode: 'time'}},
            yaxis: {{
              tickFormatter: function(val, axis) {{
                return val < axis.max ? val / 1e9 : "bISK";
              }}
            }}
          }}
        );
      }})
    }});
    </script>


Просмотр кошелька RAISA SRP
===========================

Баланс на {date}:
    {balance}

.. csv-table:: Последние выплаты по страховке:
    :class: compens

    {compens_table}
