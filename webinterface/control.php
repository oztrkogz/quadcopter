<html>
<meta http-equiv='cache-control' content='no-cache'>
<meta http-equiv='expires' content='0'>
<meta http-equiv='pragma' content='no-cache'>
<body>
<table style="width:600px" border="1">
  <tr>
    <td>
      <div id="map_2385853" style="width: 600px; height: 400px;"></div>
    </td>
    <td>

    </td>
  </tr>
  <tr>
    <td>
      <table style="width:100%" border="1">
        <form id="setrefform" action="" method="post">
        <tr>
          <td style="width:42%" colspan="2">
            <h3>Current Position:</h3>
          </td>
          <td style="width:42%" colspan="3">
            <h3>Reference Position:</h3>
          </td>
        </tr>
        <tr>
          <td style="width:21%">
            <p>Latitude:</p>
          </td>
          <td style="width:21%">
            <p id="x"></p>
          </td>
          <td style="width:21%">
            <p>Latitude:</p>
          </td>
          <td style="width:21%">
            <input type="text" name="reflatitude" value="undefined" size="13" readonly required/>
          </td>
          <td rowspan="3" style="width:16%">
            <input type="submit" value="Set Reference" /><br/>
            <input type="reset" value="Reset Values">
          </td>
        </tr>
        <tr>
          <td>
            <p>Longitude:</p>
          </td>
          <td>
            <p id="y"></p>
          </td>
          <td>
            <p>Longitude:</p>
          </td>
          <td>
            <input type="text" name="reflongtitude" value="undefined" size="13" readonly required/>
          </td>
        </tr>
        <tr>
          <td>
            <p>Altitude:</p>
          </td>
          <td>
            <p id="z"></p>
          </td>
          <td>
            <p>Altitude:</p>
          </td>
          <td>
            <input type="text" name="refaltitude" value="undefined" size="13" pattern=".{,3}" required/>
          </td>
        </tr>
        </form>
      </table>
    </td>
  </tr>
</table>

<script src="http://maps.google.com/maps/api/js?sensor=false" type="text/javascript"></script>
<script src="mapscript.js" type="text/javascript"></script>

<?php session_start(); /* Starts the session */

if(!isset($_SESSION['UserData']['Username'])){
	header("location:index.php");
	exit;
}

/*ENTERING A REFERENCE POSITION*/
if(isset($_POST['reflatitude']) && isset($_POST['reflongtitude']) && isset($_POST['refaltitude'])){
   $reflatitude = $_POST['reflatitude'];
   $reflongtitude = $_POST['reflongtitude'];
   $refaltitude = $_POST['refaltitude'];
   $reffile = fopen('refposition', 'w');
   fwrite($reffile, $reflatitude.",".$reflongtitude.",".$refaltitude);
   fclose($reffile);
}

?>
<br/>
<a href="logout.php">Logout</a>
</body>
</html>
