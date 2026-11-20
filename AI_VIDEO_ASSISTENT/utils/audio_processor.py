
import yt_dlp
from pydub import AudioSegment
import os



# AudioSegment.converter = (
# r"C:\Users\Dell\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0-full_build\bin\ffmpeg.exe"
# )

# AudioSegment.ffprobe = (
# r"C:\Users\Dell\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0-full_build\bin\ffprobe.exe"
# )

DOWNLOAD_DIR='downloades'
os.makedirs(DOWNLOAD_DIR,exist_ok=True)


def download_youtube_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "ffmpeg_location": r"C:\Users\Dell\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0-full_build\bin",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename

# data=download_youtube_audio("https://www.youtube.com/watch?v=oJrnqFfd6f0")



# because i want to use wishper 
def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path


# data_final=convert_to_wav(data)


# covert audio and chunks
def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

# print(chunk_audio(data_final))

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
























# =============================================================================
# IMPORT REQUIRED LIBRARIES
# =============================================================================

# # Import yt_dlp library to download audio from YouTube
# import yt_dlp

# # Import AudioSegment class from pydub for audio processing
# from pydub import AudioSegment

# # Import os module for file and directory operations
# import os


# # =============================================================================
# # CREATE DOWNLOAD DIRECTORY
# # =============================================================================

# # Folder name where downloaded audio files will be stored
# DOWNLOAD_DIR = "downloads"

# # Create the folder if it doesn't exist.
# # exist_ok=True prevents an error if the folder already exists.
# os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# # =============================================================================
# # DOWNLOAD YOUTUBE AUDIO
# # =============================================================================

# def download_youtube_audio(url: str) -> str:
#     """
#     Downloads the best quality audio from a YouTube video,
#     converts it to WAV format using FFmpeg,
#     and returns the path of the generated WAV file.

#     Parameters:
#         url (str): YouTube video URL

#     Returns:
#         str: Path of the downloaded WAV file
#     """

#     # Create the output file path template.
#     # %(title)s -> YouTube video title
#     # %(ext)s   -> Original downloaded extension
#     output_path = os.path.join(
#         DOWNLOAD_DIR,
#         "%(title)s.%(ext)s"
#     )

#     # =============================================================================
#     # yt-dlp Configuration
#     # =============================================================================

#     ydl_opts = {

#         # Download only the highest quality audio
#         "format": "bestaudio/best",

#         # Output filename template
#         "outtmpl": output_path,

#         # Location of FFmpeg binaries.
#         # FFmpeg is required for audio conversion.
#         "ffmpeg_location":
#         r"C:\Users\Dell\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0-full_build\bin",

#         # Post-processing after download
#         "postprocessors": [

#             {

#                 # Extract audio using FFmpeg
#                 "key": "FFmpegExtractAudio",

#                 # Convert audio into WAV format
#                 "preferredcodec": "wav",

#                 # Preferred audio quality
#                 "preferredquality": "192",
#             }

#         ],

#         # Hide unnecessary yt-dlp logs
#         "quiet": True,
#     }

#     # =============================================================================
#     # Download Audio
#     # =============================================================================

#     # Create a YouTubeDL object using the above configuration
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:

#         # Download the audio and return metadata
#         info = ydl.extract_info(
#             url,
#             download=True
#         )

#         # Generate the output filename
#         filename = ydl.prepare_filename(info)

#         # Replace the original extension with ".wav"
#         filename = (
#             filename
#             .replace(".webm", ".wav")
#             .replace(".m4a", ".wav")
#         )

#     # Return the final WAV file path
#     return filename


# # =============================================================================
# # Example Usage
# # =============================================================================

# # Uncomment the following line to test YouTube downloading

# # audio_path = download_youtube_audio(
# #     "https://www.youtube.com/watch?v=oJrnqFfd6f0"
# # )


# # =============================================================================
# # CONVERT AUDIO TO WHISPER-COMPATIBLE WAV FORMAT
# # =============================================================================

# def convert_to_wav(input_path: str) -> str:
#     """
#     Converts any audio or video file into a Whisper-compatible WAV file.

#     Whisper works best with:
#         • WAV format
#         • Mono (1 audio channel)
#         • 16 kHz sampling rate

#     Parameters:
#         input_path (str): Path of the input audio/video file.

#     Returns:
#         str: Path of the converted WAV file.
#     """

#     # -------------------------------------------------------------------------
#     # Create the output filename.
#     #
#     # Example:
#     # lecture.mp3
#     # becomes
#     # lecture_converted.wav
#     # -------------------------------------------------------------------------

#     output_path = (
#         os.path.splitext(input_path)[0]
#         + "_converted.wav"
#     )

#     # -------------------------------------------------------------------------
#     # Load the input file.
#     #
#     # AudioSegment automatically detects the file format.
#     # Supported formats include:
#     # MP3, MP4, WAV, M4A, AAC, FLAC, etc.
#     # -------------------------------------------------------------------------

#     audio = AudioSegment.from_file(input_path)

#     # -------------------------------------------------------------------------
#     # Convert Stereo → Mono
#     #
#     # Stereo = 2 channels
#     # Mono   = 1 channel
#     #
#     # Whisper works efficiently with mono audio.
#     # -------------------------------------------------------------------------

#     audio = audio.set_channels(1)

#     # -------------------------------------------------------------------------
#     # Set Sampling Rate
#     #
#     # Convert audio to 16 KHz.
#     #
#     # Whisper's recommended sample rate is 16000 Hz.
#     # -------------------------------------------------------------------------

#     audio = audio.set_frame_rate(16000)

#     # -------------------------------------------------------------------------
#     # Export the processed audio.
#     #
#     # Save it as a WAV file.
#     # -------------------------------------------------------------------------

#     audio.export(
#         output_path,
#         format="wav"
#     )

#     # Return the converted file path.
#     return output_path


# # =============================================================================
# # Example
# # =============================================================================

# # converted_file = convert_to_wav("lecture.mp4")
# # print(converted_file)


# # =============================================================================
# # SPLIT LARGE AUDIO INTO SMALL CHUNKS
# # =============================================================================

# def chunk_audio(
#     wav_path: str,
#     chunk_minutes: int = 10
# ) -> list:
#     """
#     Splits a large WAV audio file into smaller chunks.

#     Why?
#     ----
#     Large audio files require more memory and take longer to process.

#     Instead of sending a 2-hour recording to Whisper at once,
#     we split it into multiple 10-minute chunks.

#     Parameters
#     ----------
#     wav_path : str
#         Path of the WAV audio file.

#     chunk_minutes : int
#         Length of each chunk in minutes.
#         Default = 10 minutes.

#     Returns
#     -------
#     list
#         A list containing paths of all generated chunks.
#     """

#     # -------------------------------------------------------------------------
#     # Load the WAV file
#     # -------------------------------------------------------------------------

#     audio = AudioSegment.from_wav(wav_path)

#     # -------------------------------------------------------------------------
#     # Convert chunk duration from minutes to milliseconds.
#     #
#     # Why milliseconds?
#     #
#     # pydub works internally in milliseconds.
#     #
#     # Formula:
#     #
#     # minutes × 60 × 1000
#     # -------------------------------------------------------------------------

#     chunk_ms = chunk_minutes * 60 * 1000

#     # -------------------------------------------------------------------------
#     # Empty list to store chunk file paths.
#     # -------------------------------------------------------------------------

#     chunks = []

#     # -------------------------------------------------------------------------
#     # Loop through the audio.
#     #
#     # Example:
#     #
#     # Audio Length = 25 minutes
#     #
#     # start values:
#     #
#     # 0
#     # 600000
#     # 1200000
#     #
#     # (each value is in milliseconds)
#     # -------------------------------------------------------------------------

#     for i, start in enumerate(

#         range(
#             0,
#             len(audio),
#             chunk_ms
#         )

#     ):

#         # ---------------------------------------------------------------------
#         # Extract one chunk
#         # ---------------------------------------------------------------------

#         chunk = audio[start:start + chunk_ms]

#         # ---------------------------------------------------------------------
#         # Create chunk filename
#         #
#         # Example:
#         #
#         # lecture.wav_chunk_0.wav
#         # lecture.wav_chunk_1.wav
#         # lecture.wav_chunk_2.wav
#         # ---------------------------------------------------------------------

#         chunk_path = f"{wav_path}_chunk_{i}.wav"

#         # ---------------------------------------------------------------------
#         # Save chunk as WAV
#         # ---------------------------------------------------------------------

#         chunk.export(
#             chunk_path,
#             format="wav"
#         )

#         # ---------------------------------------------------------------------
#         # Store chunk path
#         # ---------------------------------------------------------------------

#         chunks.append(chunk_path)

#     # -------------------------------------------------------------------------
#     # Return list of all chunk paths
#     # -------------------------------------------------------------------------

#     return chunks


# # =============================================================================
# # Example
# # =============================================================================

# # chunks = chunk_audio("lecture_converted.wav")

# # print(chunks)

# "The chunk_audio() function divides a large WAV file into fixed-duration chunks, 
# with a default size of 10 minutes. Since pydub works in milliseconds, the chunk 
# size is converted accordingly. The function iterates through the audio, 
# extracts each segment, saves it as a separate WAV file, and returns a list of chunk paths. 
# This approach improves memory efficiency and allows long recordings to be transcribed 
# reliably by Whisper."


# # =============================================================================
# # MAIN CONTROLLER FUNCTION
# # =============================================================================

# def process_input(source: str) -> list:
#     """
#     Processes the user's input and prepares audio for Whisper.

#     Workflow:
#     ---------
#     1. Check whether the input is a YouTube URL or a local file.
#     2. If it is a YouTube URL:
#          - Download the audio.
#     3. If it is a local file:
#          - Convert it into Whisper-compatible WAV format.
#     4. Split the WAV file into smaller chunks.
#     5. Return the list of chunk file paths.

#     Parameters
#     ----------
#     source : str
#         Either:
#         • A YouTube URL
#         • A local audio/video file path

#     Returns
#     -------
#     list
#         List of generated WAV chunk file paths.
#     """

#     # -------------------------------------------------------------------------
#     # Check whether the source is a YouTube URL.
#     #
#     # startswith() checks the beginning of the string.
#     # -------------------------------------------------------------------------

#     if source.startswith("http://") or source.startswith("https://"):

#         # Display a message in the console
#         print("Detected YouTube URL.")

#         # Inform the user that the download has started
#         print("Downloading audio...")

#         # Download audio and convert it to WAV
#         wav_path = download_youtube_audio(source)

#     # -------------------------------------------------------------------------
#     # Otherwise treat the input as a local file.
#     # -------------------------------------------------------------------------

#     else:

#         # Inform the user that a local file was detected
#         print("Detected local file.")

#         # Convert the local file into Whisper-compatible WAV
#         print("Converting to WAV format...")

#         wav_path = convert_to_wav(source)

#     # -------------------------------------------------------------------------
#     # Split the WAV file into smaller chunks.
#     # -------------------------------------------------------------------------

#     print("Chunking audio...")

#     chunks = chunk_audio(wav_path)

#     # -------------------------------------------------------------------------
#     # Display the number of chunks created.
#     # -------------------------------------------------------------------------

#     print(f"Audio ready! {len(chunks)} chunk(s) created.")

#     # -------------------------------------------------------------------------
#     # Return the chunk file paths.
#     # -------------------------------------------------------------------------

#     return chunks


# # =============================================================================
# # Example Usage
# # =============================================================================

# # Example 1: YouTube URL
# # chunks = process_input(
# #     "https://www.youtube.com/watch?v=oJrnqFfd6f0"
# # )

# # Example 2: Local File
# # chunks = process_input(
# #     "lecture.mp4"
# # )

# # Print all generated chunk paths
# # print(chunks)

 


