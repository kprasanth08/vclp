html_head_template = '''
<!DOCTYPE html>
<html lang="en">

<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" type="text/css" href="./css/bootstrap.min.css">
  <link rel="stylesheet" type="text/css" href="./css/jquery.dataTables.min.css">

  <script src="./js/jquery.min.js"></script>
  <script src="./js/jquery.dataTables.min.js"></script>
  <script src="./js/_tag_.js"></script>
</head>
<body>
<div class="container">
    <h2 align="center">DEKEL</h2>
    <h3 align="center">ISO Violations</h3>
</div>

</body>
_summary_
_table_
</html>
'''

html_table_template = '''
<body>

  <div class="container">
     <br>
    <h4 style="color:#03abff" style="font-family: serif" > Affected by driver node  _driver_ </h4>
    <table id="_tag_" class="stripe" style="width:100%">
      <thead>
        <tr>
          <th>Strategies</th>
          <th>UPF Enables</th>
        </tr>
      </thead>
    </table>

  </div>

  <script>
    $(document).ready(function () {
      $('#_tag_').DataTable({
        data: _tag_,
        "searching": false,
        paging: false,
        columns: [{
            title: "Strategies"
          },
          {
            title: "UPF Enables"
          },
        ]
      });
    });
  </script>
</body>'''
html_path_table_template = '''

<body>

  <div class="container">
     <br>
    <h4 style="color:#03abff" style="font-family: serif" > Trace Path Details for _driver_ </h4>
    <table id="_trace_path_" class="stripe" style="width:100%">
      <thead>
        <tr>
          <th>Flow Path</th>
          <th>Transit Point</th>
          <th>Aided Help</th>
        </tr>
      </thead>
    </table>

  </div>
  <script>
    $(document).ready(function () {
      $('#_trace_path_').DataTable({
        data: _trace_path_,
        "searching": false,
        paging: false,
        columns: [
                 {
            title: "Aided Help"
          },
        {
            title: "Flow Path"
          },
          {
            title: "Transit Point"
          },

        ]
      });
    });
  </script>
</body>
'''

html_summary_data = '''
<body>

  <div class="container">
      <input class="form-control" id="myInput" type="text" placeholder="Search..">
    <br>

    <table id="_summ_tag_" class="stripe" style="width:100%">
      <thead>
        <tr>
          <th>Driver Node</th>
          <th>Driven By</th>
          <th>Strategies Affected</th>
          <th>Most Probable ISO Enable</th>
        </tr>
      </thead>
    </table>
  </div>

  <script>
    $(document).ready(function () {
      $('#_summ_tag_').DataTable({
        data: _summ_tag_,
        "searching": false,
        columns: [{
            title: "Driver Node"
          },
          {
            title: "Driven By"
          },
          {
            title: "Strategies Affected"
          },
          {
            title: "Most Probable ISO Enable"
          },
        ]
      });
      $("#myInput").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#_summ_tag_ tr").filter(function () {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });
    });
  </script>
</body>'''