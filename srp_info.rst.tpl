.. Файл srp_info.rst автоматически генерируется из файла srp_info.rst.tpl


Просмотр кошелька New Galaxy Age SRP
====================================

Баланс на {date}:
    {balance}

.. raw:: html

    <div id="chart" style="width: 588px; height: 300px;"></div>

    <script src="http://cdnjs.cloudflare.com/ajax/libs/flot/0.8.1/jquery.flot.min.js"></script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/flot/0.8.1/jquery.flot.time.min.js"></script>

    <script>
    $(function() {{
      $.getJSON('srp.json', function(data) {{
        $.plot("#chart", [data], {{
          xaxis: {{mode: 'time'}},
          yaxis: {{
            tickFormatter: function(val, axis) {{
              return val < axis.max ? val / 1e9 : "bISK";
            }}
          }}
        }});
      }})
    }});
    </script>


.. csv-table:: Последние выплаты по страховке:
    :escape: \

    {compens_table}
