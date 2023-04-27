# Smartcard power side channel measurement script
# Authors: Marina Shchavleva, Filip Kodytek, Jiri Bucek

# pip install pyvisa pyvisa-py pyusb
# pip install pyscard
import random
from time import sleep
import card
import oscilloscope


def list_resources(resources: list, resource_name: str):
    if not resources:
        print('no', resource_name, 'available')
    else:
        print('available', resource_name + ':')
        for resource_id in range(len(resources)):
            print('[', resource_id, '] ', resources[resource_id])

def list_scopes():
    found_oscilloscopes = oscilloscope.get_oscilloscopes()
    list_resources(found_oscilloscopes, 'oscilloscopes')


def list_readers():
    found_readers = card.get_readers()
    list_resources(found_readers, 'readers')

# def channel_meas(scope, n):
#     scope.command_check(":WAVeform:SOURce", 'CHANnel{}'.format(n))
#     trace = scope.query_binary(':WAVeform:DATA?')
#     return trace

def printscreen(scope: oscilloscope):
    with open ('printscreen.png', "wb") as fscreen:
        # /* Download the screen image */
        scope.write(":HARDcopy:INKSaver OFF")
        # /* Read screen image. */
        screen_data = scope.query_binary(":DISPlay:DATA? PNG, COLor")
        fscreen.write(screen_data)

# Infinite test run. Can be interrupted by pressing CTRL-C
def test_run(my_card: card):
    print ("Infinite run, press CTRL-C to break.")
    try:
        while True:
            my_card.send_encrypt([i for i in range(16)])
            sleep(0.01)
    except KeyboardInterrupt:
        pass
    

def measure_random(scope: oscilloscope, my_card: card, num_of_measurements):
    with open('traceLength.txt', "w") as finfo, open ('traces.bin', "wb") as fdata,\
        open('plaintext.txt',"w") as fplaintext, open('ciphertext.txt',"w") as fciphertext:
        scope.command_check(":ACQuire:TYPE", "NORMal")
        scope.command_check(":TIMebase:MODE", "MAIN")
        scope.command_check(":WAVeform:UNSigned", "1")
        scope.command_check(":WAVeform:BYTeorder", "LSBFirst")
        scope.command_check(":WAVeform:FORMat", "BYTE")
        scope.command_check(":WAVeform:POINts:MODE", "RAW")
        scope.command_check(":ACQuire:COMPlete", "100")
        scope.command_check(":WAVeform:SOURce", 'CHANnel2')

        # Requested points per trace - change if necessary. 
        # If less points are required, you can set the limit here.
        # If more points are required, disable channel 1 on the scope (trigger will still work)
        # If you need yet more points, change the overall settings to use the SRAT command.
        scope.write(":WAVeform:POINts MAX") 
        
        print("Warmup cycle")
        # put something on screen:
        scope.write(':RUN')
        #dummy card op - wake up card, warm up
        for i in range(100):
            my_card.send_encrypt([i for i in range(16)])

        print("Measurement cycle")
        # Measurement cycle
        for i in range(num_of_measurements):
            card_pt = list(random.randbytes(16))
            print(f"Trace {i}")
            scope.write(':SINGle')
            sleep(0.05) # Wait for the scope to arm its trigger
            card_ct = my_card.send_encrypt(card_pt) 
            sleep(0.05)
            # trace = scope.query_binary(':WAVeform:DATA?')
            r=scope.resource
            r.write(":WAV:DATA?")
            head_2bytes = r.read_bytes(2)
            assert(head_2bytes[0:1] == b'#')
            digits=int(head_2bytes[1:])
            length=int(r.read_bytes(digits))
            trace=r.read_bytes(length, chunk_size=length)
            r.read_bytes(1) # read delimite
            trace = scope.query_binary(':WAVeform:DATA?')
            if i == 0:
                tracelength = scope.query(':WAVeform:POINts?')
                print(tracelength, file = finfo)
            fdata.write(trace)
            print(" ".join(map(lambda b: "%02x" % b, card_pt)), file = fplaintext)
            print(" ".join(map(lambda b: "%02x" % b, card_ct)), file = fciphertext)


# =============================== MAIN ===================================
if __name__ == '__main__':
    list_scopes()
    list_readers()
    print('----------------')
    scope = oscilloscope.Oscilloscope()
    reader = card.Reader()
    print(reader.send_encrypt([i for i in range(16)]))

    print('------- DUMMY TEST, SET UP YOUR SCOPE ---------')
    # test_run(reader)

    # scope.save_conf('scope_setup.conf')
    # printscreen(scope)

    # scope.load_conf('scope_setup.conf')

    print('------- MEASUREMENT WITH CARD AND SCOPE ---------')
    measure_random(scope, reader, 1000)


