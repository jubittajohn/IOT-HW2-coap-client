# CoAP CLIENT excecution
The file IOT_HW2-coap-client has the following data:
- Client.py - Program code for coap client

## Library used
- aiocoap in python

## Required installations
- install aiocoap library using the following command

    ```  pip3 install aiocoap```

## How to excute CoAP client
- Run ifconfig and find out the ip address of system the client file is on. Edit the Client.py and change the value of HOST_NAME in line 8 to the ip address.
- Make sure Client system is connected on the same LAN as the server.
- Assuming the server is now already up and running, start the Client.py. 
- Now the client requests for 100B, 10KB and 1MB files the reuired number of times.
- To transfer 10MB files uncomment line 59 and comment line 58 in Client.py

    line 59: ```filename_count = {'10MB':10}```

    line 58 : ```filename_count = {'100B':10000, '10KB':1000, '1MB':100} ```

## What happens in CoAP client
- At first folder structures will be created to store the files received from the server. The folder DataRecieved is created with 4 subfolders inside it named 100B, 10KB, 1MB and 10MB to store the respective size folders.
- Running the Client.py two times with line59 and line 58 will transfer the files of size 100B, 10KB, 1MB and 10MB the required number of times.
- The files will be stored inside the respective size folder with the name {filesize}_{filecount}. For example the 99th 100B transfered file will be stired inside the folder DataReceived/100B as 100B_99.
- Data is recieved and written into file as chunks of size 64KB.
- After total number of each file is transferred the following is output: 
    - Average throughput
    - Standard deviation of  throughput
    - Average total application layer data
- Throughput is calculated by taking the average of each filesize divided by time taken for transfer. The time taken for transfer is calculated by finding the difference in time before start and end of transferred data obtained by calling time.time().
- Standard deviation is calculated by calling the inbuilt function statistics.stdev()
- Total application layer data transferred is calculated by the dividing the total size of payload by the actual file size. actual file size is obtained by os.path.getsize() function and size of payload is obtained by adding actual file size and header size. Header size is hard coded as 4 bytes as the hedaer size for CoAP is 4 bytes.