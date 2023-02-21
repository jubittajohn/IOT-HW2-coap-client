import aiocoap
import asyncio
import os
import logging
import statistics
import time

HOST_NAME = "192.168.0.19"
logging.basicConfig(level=logging.INFO)

def createFolderStructure():
    folder_name = "DataReceived"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    filenames = ['100B', '10KB', '1MB', '10MB']
    for subfolder in filenames:
        subfolder_name = os.path.join(folder_name, subfolder)
        if not os.path.exists(subfolder_name):
            os.mkdir(subfolder_name)

def calculations(timesSend, throughput, totalDataTrans_by_fileSize):

    #delete the element with 0 value coz file transer didn't happen successfully
    delCount = 0
    for i, x in enumerate(throughput):
        if x == 0:
            throughput.pop(i)
            delCount += 1

    for i, x in enumerate(totalDataTrans_by_fileSize):
        if x == 0:
            totalDataTrans_by_fileSize.pop(i)
    timesSend = timesSend - delCount        

    #average throughput calculation
    sumTime = 0
    for x in throughput:
        sumTime += x
    averageTP = sumTime/timesSend 
    print("Average throughput = ", averageTP)

    #standard deviation of throughput
    stdDev = statistics.stdev(throughput)
    print("Standard deviation of  throughput = ", stdDev)

    #average application layer data transferred calculation
    sumData = 0
    for x in totalDataTrans_by_fileSize:
        sumData += x
    averageALD = sumData/timesSend
    print("Average total application layer data = ", averageALD)

async def download_file():
    context = await aiocoap.Context.create_client_context()
    
    dataTrans = ""
    filename_count = {'100B':10000, '10KB':1000, '1MB':100} 
    #filename_count = {'10MB':10}
    for filename, timesSend in filename_count.items():
        print("\n File Size: ",filename, " \n")
        throughput = [0] * timesSend
        totalDataTrans_by_fileSize = [0] * timesSend
        filepath = os.path.join('DataReceived',filename)
        count = 1
        while count <= timesSend:
            new_filename = filename + '_' + str(count)
            filepath1 = os.path.join(filepath, new_filename)
            start = time.time()
            request = aiocoap.Message(code=aiocoap.PUT, payload=filename.encode('utf-8'), uri='coap://{}/file'.format(HOST_NAME),  mtype=aiocoap.CON)
            with open(filepath1, 'wb') as f:
                try:
                    response = await context.request(request).response
                except Exception as e:
                    print('Failed to fetch resource:')
                    print(e)
                else:
                    f.write(response.payload)
            end = time.time()
            filesize = os.path.getsize(filepath1)
            if filesize!=0:
                throughput[count-1] = (8 * filesize) / ((end - start)*1000)
                dataTrans = 4 + filesize
                totalDataTrans_by_fileSize[count-1] = dataTrans/filesize              
            count += 1
        calculations(timesSend, throughput, totalDataTrans_by_fileSize)
    await context.shutdown()

if __name__ == "__main__":

    #create folder structure for storing data
    createFolderStructure()
    asyncio.get_event_loop().run_until_complete(download_file())
