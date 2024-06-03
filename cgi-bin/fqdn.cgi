#!/bin/bash

echo 'Content-type: text/html'

echo '
<!DOCTYPE html>

<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="/bootstrap/bootstrap-5.3.3-dist/css/bootstrap-grid.min.css" rel="stylesheet">
  <link href="/bootstrap/css/estilo-cgi.css" rel="stylesheet">
  <title>Enviar Arquivo CSV</title>
</head>

<body>

<div class="container">
  <h1>Enviar FQDN CSV</h1>
  <div class="form-container">
    <p>Formato: Nome;url.domain</p>
    <form action="/cgi-bin/fqdn_csv.cgi" method="post" enctype="multipart/form-data">
      <label for="csv_file">Escolher Arquivo</label>
      <input type="file" id="csv_file" name="csv_file" accept=".csv" required>
      <div id="file-name">Nenhum arquivo escolhido</div>
      <button type="submit">Enviar</button>
    </form>
  </div>
</div>

<script>
  document.getElementById("csv_file").addEventListener("change", function() {
    var fileName = this.files[0] ? this.files[0].name : "Nenhum arquivo escolhido";
    document.getElementById("file-name").textContent = fileName;
  });
</script>

</body>

</html>
'

