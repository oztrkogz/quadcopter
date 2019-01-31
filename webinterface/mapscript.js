  var curlocation = new Array();
  var reflocation = new Array();
  var reflocstring;
  var map = new google.maps.Map(document.getElementById('map_2385853'), {
    zoom: 15,
    minZoom: 15,
    streetViewControl: false,
    center: new google.maps.LatLng(41.106000, 29.026233),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  loadCurposition(); 
  var curmarker = new google.maps.Marker({
     map: map
  });

  loadRefposition();
  var refmarker = new google.maps.Marker({
     map: map,
     draggable: true,
     icon: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'
  });

  function loadCurposition() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var curlocstring = this.responseText.split(",");
        curlocation = [parseFloat(curlocstring[0]), parseFloat(curlocstring[1]), parseFloat(curlocstring[2])];
        curmarker.setPosition(new google.maps.LatLng(curlocation[0], curlocation[1]));

        document.getElementById("x").innerHTML = curlocation[0];
        document.getElementById("y").innerHTML = curlocation[1];
	document.getElementById("z").innerHTML = curlocation[2];
      }
    };
    xhttp.open("GET", "curposition", true);
    xhttp.send();
  }

  setInterval('loadCurposition()',1000);

  function loadRefposition() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var reflocstring = this.responseText.split(",");
        if (reflocstring[0] != "undefined" && reflocstring[1] != "undefined") {
          reflocation = [parseFloat(reflocstring[0]), parseFloat(reflocstring[1])];
          refmarker.setPosition(new google.maps.LatLng(reflocation[0], reflocation[1]));
        }
        else {
        reflocation[0] = reflocstring[0];
	reflocation[1] = reflocstring[1];
        }
	if (reflocstring[2] != "undefined") {
        reflocation[2] = parseFloat(reflocstring[2]);
        }
	else {
	reflocation[2] = reflocstring[2];
        }
        setrefform.elements["reflatitude"].value = reflocation[0];
        setrefform.elements["reflongtitude"].value = reflocation[1];
        setrefform.elements["refaltitude"].value = reflocation[2];
      }
    };
    xhttp.open("GET", "refposition", true);
    xhttp.send();
  }

  google.maps.event.addListener(map,'click',function(event) {
    refmarker.setPosition(event.latLng);
    refmarker.setMap(map);
    reflocstring = event.latLng;
    reflocation[0] = Number(reflocstring.lat().toFixed(6));
    reflocation[1] = Number(reflocstring.lng().toFixed(6));
    setrefform.elements["reflatitude"].value = reflocation[0];
    setrefform.elements["reflongtitude"].value = reflocation[1];
  });

  google.maps.event.addListener(refmarker,'dragend',function(event) {
    refmarker.setPosition(event.latLng);
    refmarker.setMap(map);
    reflocstring = event.latLng;
    reflocation[0] = Number(reflocstring.lat().toFixed(6));
    reflocation[1] = Number(reflocstring.lng().toFixed(6));
    setrefform.elements["reflatitude"].value = reflocation[0];
    setrefform.elements["reflongtitude"].value = reflocation[1];
  });

  google.maps.event.addListener(refmarker,'dblclick',function() {
    refmarker.setMap(null);
    refmarker.setPosition(null);
    reflocation[0] = "undefined";
    reflocation[1] = "undefined";
    setrefform.elements["reflatitude"].value = reflocation[0];
    setrefform.elements["reflongtitude"].value = reflocation[1];
  });
