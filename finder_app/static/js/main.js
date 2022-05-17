var map, city_dict;

var current_id = null;
var lines = [];


var shake_animation = [
  { transform: 'translateX(0)' },
  { transform: 'translateX(5px)' },
  { transform: 'translateX(10px)' },
  { transform: 'translateX(0px)' },
  { transform: 'translateX(-10px)' },
  { transform: 'translateX(-5px)' },
  { transform: 'translateX(0)' },
];

var shake_timing = {
  duration: 500,
  iterations: 1,
}


var pop_up_cont = document.getElementById("pop_up_cont");

function render(data) {

  var data = data

  console.log("rendering nodes ...");

  const starting_lat_lng = { lng: parseFloat(data.view_lng), lat: parseFloat(data.view_lat) };

  map = new google.maps.Map(document.getElementById("map"), {
    center: starting_lat_lng,
    zoom: data.view_zoom,
    mapId: "47beb21b23161ed8"
  });

  city_dict = {}

  for (const node of data.graph.nodes) {

    const LatLng = { lng: parseFloat(node.longitude), lat: parseFloat(node.latitude) };

    city_dict[node.id] = LatLng;

    const marker = new google.maps.Marker({
      position: LatLng,
      map,
      title: node.id,
    });

    marker.addListener("click", () => {
      marker_clicked(marker.getTitle());
      console.log("MARKER CLICKED: " + marker.getTitle());

      // animate
      marker.setAnimation(google.maps.Animation.BOUNCE);

      setTimeout(function () {
        marker.setAnimation(null);
      }, 500);

    });

  }

  const cost_limit = document.getElementById("cost_limit_slider").value * 1000;

  for (const edge of data.graph.links) {

    const line_coords = [
      city_dict[edge.source],
      city_dict[edge.target]
    ];

    const line = new google.maps.Polyline({
      path: line_coords,
      geodesic: true,
      strokeColor: "#666677",
      strokeOpacity: 1.0,
      strokeWeight: 0.7,
    });

    lines.push({
      "line_obj": line,
      "cost": edge.driving_cost
    })

    if (edge.driving_cost > cost_limit) {
      line.setMap(null);
      continue;
    }

    line.setMap(window.map);
  }
}

function update_edges(cost_limit) {

  for (const line_dict of lines) {

    if (line_dict.cost > cost_limit * 1000) {
      line_dict.line_obj.setMap(null);
    } else {
      line_dict.line_obj.setMap(window.map);
    }

  }

}


function initMap() {

  fetch('/load_graph')
    .then(response => response.json())
    .then(data => render(data));
}

function marker_clicked(marker_name) {

  


  src_city_label = document.getElementById("src_city");
  dest_city_label = document.getElementById("dest_city");

  if (window.selected_nodes.length == 0) {
    src_city_label.value = marker_name;
    src_city_label.animate(shake_animation, shake_timing);
    window.selected_nodes.push(marker_name);
  }
  else if (window.selected_nodes.length == 1) {

    if (src_city_label.value == marker_name) {
      src_city_label.value = "";
      window.selected_nodes = [];
      src_city_label.animate(shake_animation, shake_timing);
      return;
    }

    dest_city_label.value = marker_name;
    dest_city_label.animate(shake_animation, shake_timing);
    window.selected_nodes.push(marker_name);
  } else {

    let dest_cities = dest_city_label.value.split(", ");

    if (dest_cities[dest_cities.length - 1] == marker_name) {

      dest_cities.pop();
      window.selected_nodes.pop(); 

      dest_city_label.value = dest_cities.join(", ");
      dest_city_label.animate(shake_animation, shake_timing);
      return;
    }
    dest_cities.push(marker_name);
    window.selected_nodes.push(marker_name)

    src_city_label.value = window.selected_nodes[0];
    dest_city_label.value = dest_cities.join(", ");

    src_city_label.animate(shake_animation, shake_timing);
    dest_city_label.animate(shake_animation, shake_timing);
  }


}



function OpenPathPopUp() {

  path_form = document.getElementById("path_form");

  const xhr = new XMLHttpRequest();
  var FD = new FormData(path_form);

  // Define what happens on successful data submission
  xhr.addEventListener('load', function (event) {

    remove_old_path();

    if (xhr.status == 400) { // analyze HTTP status of the response

      json_res = JSON.parse(this.responseText);

      var alert_text = 'Invalid Input\n\n';
      for (const err of json_res.errors) {
        alert_text += "\t• " + err.name + ": " + err.error + "\n";
      }
      alert_text += "\n";

      alert(alert_text);

      return;


    } else if (xhr.status == 200) { // show the result

      var modal = document.getElementById("path_pop_up");
      modal.style.display = "block";
      window.pop_up_cont.style.display = "flex";

      document.getElementById("map").classList.add("blur");

      json_res = JSON.parse(this.responseText);
      view_path_in_pop_up(json_res);
      return;
    } else if (xhr.status == 404 || xhr.status == 406 || xhr.status == 508) { // show the result

      alert(JSON.parse(this.responseText).msg);
      return;
    }
    alert(xhr.responseText)
  });

  // Define what happens in case of error
  xhr.addEventListener(' error', function (event) {
    alert('Oops! Something went wrong.');
  });

  // Set up our request
  xhr.open('POST', '/get_path');

  // Send our FormData object; HTTP headers are set automatically
  xhr.send(FD);

}

function view_path_in_pop_up(json_response) {

  window.latest_response = json_response;

  document.getElementById("accumulated_cost").innerHTML = json_response.accumulated_cost;
  document.getElementById("cost_mode").innerHTML = json_response.mode;

  document.getElementById("other_cost_1_name").innerHTML = json_response.other_cost_1_name;
  document.getElementById("other_cost_1_value").innerHTML = json_response.other_cost_1_value;

  document.getElementById("other_cost_2_name").innerHTML = json_response.other_cost_2_name;
  document.getElementById("other_cost_2_value").innerHTML = json_response.other_cost_2_value;

  var p_d = document.getElementById("path_data");

  p_d.innerHTML = "";
  var i = 0
  for (const point of json_response.path) {
    var path_point = document.createElement("div");
    path_point.innerHTML = point;
    path_point.classList.add("path_point");

    p_d.appendChild(path_point);

    if (i < json_response.path.length - 1) {
      var step_cost = document.createElement("div");
      step_cost.innerHTML = json_response.steps_costs[i] + " m";
      p_d.appendChild(step_cost);
    }

    i++;

  }
}

function heuristic_table() {

  if (window.latest_response.heuristic_table == 0) {
    alert("No Heuristic Was Used");
    return;
  }

  var alert_text = 'Heuristic Values For Last Goal: \n\n';

  for (const entry of window.latest_response.heuristic_table) {
    alert_text += "\t• " + entry.city_name + ": " + entry.value + "m\n";
  }

  alert_text += "\n";

  alert(alert_text);
  return;

}

var p = document.getElementById("path_pop_up");

var close = document.getElementById("close_path");

close.onclick = function () {
  window.p.style.display = "none";
  window.pop_up_cont.style.display = "none";
  document.getElementById("map").classList.remove("blur");
}


var slider = document.getElementById("cost_limit_slider");
var output = document.getElementById("cost_limit_label");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function () {
  output.innerHTML = this.value;
  update_edges(this.value);
}

var path_line;

function remove_old_path() {

  if (!(path_line === undefined)) {
    path_line.setMap(null);
  }

}
function plot_path() {

  remove_old_path();

  p.style.display = "none";
  window.pop_up_cont.style.display = "none";
  document.getElementById("map").classList.remove("blur");

  const path_coords = [
  ];

  for (const city of window.latest_response.path) {
    path_coords.push(window.city_dict[city]);
  }

  path_line = new google.maps.Polyline({
    path: path_coords,
    geodesic: true,
    strokeColor: "#2E86C1",
    strokeOpacity: 1.0,
    strokeWeight: 4,
  });

  path_line.setMap(window.map);

}

function ClearCities(){

  remove_old_path();
  window.selected_nodes = [];

  src_city_label = document.getElementById("src_city");
  dest_city_label = document.getElementById("dest_city");

  src_city_label.value = "";
  dest_city_label.value = "";
  

  src_city_label.animate(shake_animation, shake_timing);
  dest_city_label.animate(shake_animation, shake_timing);

}