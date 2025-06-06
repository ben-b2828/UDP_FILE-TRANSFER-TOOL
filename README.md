UDP_FILE_TRANSFER_TOOL
Overview
The UDP File Transfer Tool is a graphical desktop application built with Python, Tkinter, and the socket library to facilitate file sharing between devices over a network using the UDP protocol. The application allows:
•	Users to send files to a specified IP and port.
•	Receivers to listen for incoming file data and save it locally.
•	Real-time notifications and logs of the transfer process.
This project is ideal for understanding how UDP works in practice, particularly the stateless, connectionless nature of this protocol.


Key Features
•	Graphical User Interface (GUI): Built with Tkinter for user-friendliness.
•	UDP Sockets: Uses socket.AF_INET and socket.SOCK_DGRAM for fast, lightweight communication.
•	File Chunking: Files are split into large chunks (60,000 bytes) and reassembled after reception.
•	Concurrent File Reception: Uses Python threads to receive files without freezing the GUI.
•	Real-Time Logs: Displays live updates in a scrollable log window.
•	Custom Save Directory: Receiver can choose where to store incoming files.
•	Multiplatform Support: Works on Windows, Linux, and macOS.
 Configuration Constants
•	CHUNK_SIZE = 60000: Controls size of each data packet.
•	TIME_BETWEEN_CHUNKS = 0.05: Delay between sending packets.
•	RECEIVE_TIMEOUT = 60: Timeout for waiting on incoming packets.
•	DEFAULT_RECEIVED_DIR = "received_files": Default folder for storing received files.
 How It Works
 File Sending Process
1.	User selects a file and inputs receiver’s IP and port.
2.	The file is read in binary mode and broken into chunks.
3.	Each chunk is prepended with a header: ID:<packet_number>:.
4.	An initial message (FILENAME:<filename>) informs the receiver of the file name.
5.	Once all packets are sent, a special __END__ packet signifies completion.
File Receiving Process
1.	The receiver clicks Start Listening on a chosen port.
2.	On receiving FILENAME:<name>, the app starts storing incoming packets in a dictionary indexed by their packet ID.
3.	When __END__ is received, all chunks are reassembled and saved to the selected directory.
 Communication Format
•	Header: ID:<packet_id>: followed by binary data.
•	Control Messages:
o	FILENAME:<filename> – file name header.
o	__END__ – transmission complete.
GUI Structure
Interface Overview
The interface consists of three main sections:
1. Sender Frame
•	Fields:
o	File path (with browse option)
o	Receiver IP address
o	Port number
•	Button: 📤 Send File
2. Receiver Frame
•	Field: Listening port
•	Buttons:
o	🟢 Start Listening (saves to default directory)
o	📥 Receive File Now (allows custom directory selection)
3. Log Area
•	Scrollable text window that shows:
o	IP resolution
o	Packet transfer status
o	Errors, warnings, and success notifications
Style & Design
•	Background colors: Blue, Green, Grey
•	Fonts: Times New Roman UI, Consolas
•	Iconic buttons for modern UI experience

 Page 5: Setup Instructions
 Requirements
•	Python 
•	Tkinter (comes pre-installed with Python)
•	No external libraries required
 Installation
1.	Clone or download the repository:
git clone https://github.com/ben-b2828/udp-file-transfer-tool.git
a. Navigate to the project folder
b. Run the application

 Notes
•	Make sure both sender and receiver are connected to the same network.
•	Firewalls and antivirus software may block UDP communication — allow access when prompted.

Limitations, Enhancements & Credits
 Limitations
•	No built-in encryption or compression.
•	Packets can be lost as UDP is not reliable — no retransmission of lost chunks.
•	No support for very large files (> hundreds of MBs) on unstable networks.
 Potential Improvements
•	Add file integrity checks (e.g., using checksums).
•	Implement packet acknowledgments and retransmission for reliability.
•	Add multi-file transfer and drag-and-drop support.
•	Add progress bars and file size indicators.

