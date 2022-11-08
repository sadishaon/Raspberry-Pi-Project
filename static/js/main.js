/**
 * Updates the current color, distance and motor status calling teh corresponding methods
 */
 function updateStatus() {
  
  // Update current distance
  updateDistance()
  
  
  // Update current color based on Open CV
  updateCurrentColorOpenCV()
  

  // Update motor status
  updateMotorStatus()
  

  // Update current distance based on color
  updateCurrentColorDistance()
}


/**
 * Update the current color based on OpenCV
 */
 async function updateCurrentColorOpenCV() {
  try {
    // Request color from server
    const requestResult = await requestColorFromOpenCV()
    // Get the HTML element where the status is displayed
    const green_open_cv = document.getElementById('green_open_cv')
    green_open_cv.innerHTML = requestResult.data[0]
    const purple_open_cv = document.getElementById('purple_open_cv')
    purple_open_cv.innerHTML = requestResult.data[1]
    const yellow_open_cv = document.getElementById('yellow_open_cv')
    yellow_open_cv.innerHTML = requestResult.data[2]
  } catch (e) {
    console.log('Error getting the color based on OpenCV', e)
    updateStatus('Error getting the color based on OpenCV')
  }
}
/**
 * Function to request the server to update the current color based on OpenCV
 */
 function requestColorFromOpenCV () {
  try {
    // Make request to server
    return axios.get('/get_color_from_opencv')
  } catch (e) {
    console.log('Error getting the status', e)
    updateStatus('Error getting the status')
  }
}


/**
 * Update the current color based on distance sensor
 */
 async function updateCurrentColorDistance() {
  try {
    // Request color from server
    const requestResult = await requestColorFromDistance()
    // Get the HTML element where the status is displayed
    const green_distance = document.getElementById('green_distance')
    green_distance.innerHTML = requestResult.data[0]
    const purple_distance = document.getElementById('purple_distance')
    purple_distance.innerHTML = requestResult.data[1]
    const yellow_distance = document.getElementById('yellow_distance')
    yellow_distance.innerHTML = requestResult.data[2]
  } catch (e) {
    console.log('Error getting the color based on distance', e)
    updateStatus('Error getting the color based on distance')
  }
}
/**
 * Function to request the server to get the color based
 * on distance
 */
 function requestColorFromDistance() {
  try {
    // Make request to server
    return axios.get('/get_color_from_distance')
  } catch (e) {
    console.log('Error getting the status', e)
    updateStatus('Error getting the status')
  }
}


/**
 * Function to request the server to update 
 * the distance measurement
 */
 async function updateDistance() {
  try {
    const requestResult = requestDistance()
  } catch (e) {
    console.log('Error getting the distance', e)
    updateStatus('Error getting the distance')
  }
}
/**
 * Function to request the server to get the distance from
 * the rod to the ultrasonic sensor
 */
 async function requestDistance () {
  //...
  try {
    // Make request to server
    let result = await axios.get('/get_distance')
    let distance = document.getElementById("distance")
    distance.innerText = result.data.distance
  } catch (e) {
    console.log('Error getting the distance request', e)
    updateStatus('Error getting the distance request')
  }
}
/**
 * Function to request the server to start the motor
 */
 function requestStartMotor () {
  try {
    // Make request to server
    return axios.get('/start_motor')
  } catch (e) {
    console.log('Error getting the start request', e)
    updateStatus('Error getting the start request')
  }
}
/**
 * Function to request the server to stop the motor
 */
 function requestStopMotor () {
  try {
    // Make request to server
    return axios.get('/stop_motor')
  } catch (e) {
    console.log('Error getting the stop request', e)
    updateStatus('Error getting the stop request')
  }
}
/**
 * Function to request the server to update the 
 * motor status with Boolean indicating
 */
async function updateMotorStatus() {
  // Make request to server
  axios.get('/motor_status')
  .then((response) => {
    const motor_status_html_element = document.getElementById('motor')
    if (response.data.success){motor_status_html_element.innerHTML = "True"}
    else{motor_status_html_element.innerHTML = "False"}
  })
}

