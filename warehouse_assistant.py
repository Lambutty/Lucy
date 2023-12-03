
import pyttsx3
import argparse
import queue
import sys
import sounddevice as sd
import json

from vosk import Model, KaldiRecognizer
from spots import Spots

class WarehouseAssistant:
    
    def __init__(self,*,
                 collection,
                 agent_name:str = "Lucy",
                 stop_phrase:str = "stop",
                 listen_for_tick_duration:int = 14,
                 speak_engine:str = "sapi5",
                 debug:bool= True,
                 insult: str = "Pisser"
                 ):
        self.stop_phrase = stop_phrase
        self.agent_name = agent_name
        self.q = queue.Queue()
        self.engine = pyttsx3.init(driverName = speak_engine) 
        self.cache = set()
        self.count = 0
        self.should_listen = False
        self.say_please = False
        self.collection = collection
        self.listen_for_tick_duration = listen_for_tick_duration
        self.debug = debug
        self.insult = insult
    
    def listen(self,text:str) -> None|str:
        if self.debug:
            print(self.cache)
        should_stop = self.stop_phrase.lower() in text
        if text == "" or should_stop:
            if self.count >= self.listen_for_tick_duration or should_stop:
                self.count = 0
                self.should_listen = False
                try:
                    search_string = max(self.cache , key = len)
                except Exception:
                    self.cache = set()
                    return None
                self.cache = set()
                return search_string
            self.count+=1
        elif text in self.cache:
            return None
        else:
            self.cache.add(text)
            return None
        
        
    def convert(self,key: str, dict_ : dict) -> str:
        return json.loads(dict_)[key]

    def check_for_agent_name(self,key: str, res: dict) -> bool:
        if self.debug:
            if(b:= self.convert(key,res).lower()):
                print(b) 
        return self.agent_name.lower() in set(self.convert(key,res).lower().split(" "))

    def callback(self,indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))
    
    def run(self):
        def int_or_str(text):
            """Helper function for argument parsing."""
            try:
                return int(text)
            except ValueError:
                return text
            
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-l", "--list-devices", action="store_true",
            help="show list of audio devices and exit")
        args, remaining = parser.parse_known_args()
        if args.list_devices:
            print(sd.query_devices())
            parser.exit(0)
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[parser])
        parser.add_argument(
            "-f", "--filename", type=str, metavar="FILENAME",
            help="audio file to store recording to")
        parser.add_argument(
            "-d", "--device", type = int_or_str,
            help="input device (numeric ID or substring)")
        parser.add_argument(
            "-r", "--samplerate", type=int, help="sampling rate")
        parser.add_argument(
            "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
        args = parser.parse_args(remaining)

        try:
            if args.samplerate is None:
                device_info = sd.query_devices(args.device, "input")
                # soundfile expects an int, sounddevice provides a float:
                args.samplerate = int(device_info["default_samplerate"])
                
            if args.model is None:
                model = Model(lang="en-us")
            else:
                model = Model(lang=args.model)

            if args.filename:
                dump_fn = open(args.filename, "wb")
            else:
                dump_fn = None

            with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype="int16", channels=1, callback=self.callback):
                print("#" * 80)
                print("Press Ctrl+C to stop the recording")
                print("#" * 80)

                rec = KaldiRecognizer(model, args.samplerate)
                while True:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        
                        if not self.say_please and self.check_for_agent_name('text', rec.Result()):
                            self.should_listen = True
                            self.say_please = True
                            self.engine.say("Bitte")
                            self.engine.runAndWait()
                        if self.should_listen and (query_text := self.listen(self.convert('text',rec.Result()))):
                            self.should_listen = False
                            results = self.collection.query(
                                    query_texts=[query_text],
                                    n_results=1,
                                    #where={"metadata_field": "document1"}, # optional filter
                                    #where_document={"$contains": "nuts"} # optional filter
                                )

                            self.engine.say(f"Sollten in {Spots.GANG.value}" + str(results['metadatas'][0][0][Spots.GANG.value]) + f"sein du {self.insult}")                    
                            self.engine.runAndWait()
                            self.say_please = False
                    else:
                        if not self.say_please and self.check_for_agent_name('partial',rec.PartialResult()):
                            self.should_listen = True
                            self.say_please = True
                            self.engine.say("Bitte")
                            self.engine.runAndWait()
                        if self.should_listen and (query_text := self.listen(self.convert('partial', rec.PartialResult()))):
                            self.should_listen = False
                            results = self.collection.query(
                                    query_texts=[query_text],
                                    n_results=1,
                                    #where={"metadata_field": "document1"}, # optional filter
                                    #where_document={"$contains": "nuts"} # optional filter
                            )
                            
                            self.engine.say(f"Sollten in {Spots.GANG.value}" + str(results['metadatas'][0][0][Spots.GANG.value]) + f"sein du {self.insult}")                    
                            self.engine.runAndWait()
                            self.say_please = False

                    self.engine.say("PS: Deine Mutter stinkt nach Wurstwasser.")    
                    if dump_fn is not None:
                        dump_fn.write(data)

        except KeyboardInterrupt:
            print("\nDone")
            parser.exit(0)
        except Exception as e:
            parser.exit(type(e).__name__ + ": " + str(e))
            