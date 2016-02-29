# gPower
Phone Grid

Routes:

1. http://smartgrid-pzero.rhcloud.com/  GET
  Welcome!

2. http://smartgrid-pzero.rhcloud.com/bts_dls/device_data  POST
   Request  - {
      "imsi": "IMSI999990091744071", 
      "pos_x": -65, 
      "pos_y": 67, 
      "rssi": -101, 
      "time": 135
}

  Response - {
  "dev_data": {
    "closest_bts": "http://gpower-pzero.rhcloud.com/bts_udp", 
      "imsi": "IMSI999990091744071", 
      "pos_x": -65, 
      "pos_y": 67, 
      "rssi": -101, 
      "time": 135
  }
}

   Bad Request Check  - missing attributes, time,x,y,rssi not numbers
   Multiple BTS - if signal strength is lower than -100 then look for a bts which covers the location of the phone i.e pos_x, pos_y and if present send the url.
  
  3. http://smartgrid-pzero.rhcloud.com/device/  GET
   list of devices
   
  4. http://smartgrid-pzero.rhcloud.com/device_data/<imsi>/ GET
  Data specific to this device
  
  5. http://smartgrid-pzero.rhcloud.com/device_data/<imsi>/signal_strength  GET
   x,y location categorised as weak(<-90),fair(-90,-70),good zones(>-70) [Approximation as per data)
   
  6.  http://smartgrid-pzero.rhcloud.com/device_data
  All data received by the bts
  
  Comments:
  
  1. Time and Location data could be used - time frequency distribution along with x,y coordinates to get an idea of device's responsiveness as per location. (I was having installation issues with numpy so left this)
  2. Tried to minimize processing during server hit to keep the throughput high. All aggregation/analytics to be done on on raw data/events.
  
  
  
  
  
  
