# CS3305 Group 11 - Project Report 
## K.L.A.A.S - Knowledge Lookup and Archive Access Service

## Introduction  
  
Our application, File Explorer, Organiser and Sharing (K.L.A.A.S), is designed to streamline the user's interaction with their local filesystem and enhance file management, sharing, and optimisation. It allows users to not only manage their files locally but also to share them via a built-in web server powered by Flask, a lightweight WSGI web application framework.  

Our system offers a practical solution for automating and regulating the way in which files systems are organised. It aligns with real-world scenarios where in this digital age there is a growing necessity for personal storage optimisation and instant file sharing. The primary functionalities of this application including organisation, optimisation, file visualisation and sharing, all work towards this common goal.
## Project Objectives  
  
The objectives of the project are as follows:  
  
1. To develop a unified platform that simplifies file management through automatic sorting, in-depth organisation, and scheduling features.  
2. To enable efficient file sharing capabilities through a cloud-based system, allowing users to share files with external parties securely.  
3. To implement advanced file optimisation techniques such as compression and deduplication, thereby enhancing storage efficiency and organisation.  
  
## Architecture  
  
The architecture of K.L.A.A.S is modular, consisting of three primary components: the Desktop Client, the Flask Web Server(including the Expiry Service), and the WebUI client. The modular architecture of K.L.A.A.S not only ensures a separation of concerns for better manageability and scalability but also allows for the continuous development and enhancement of individual components without disrupting the entire system. This structure supports the evolution of K.L.A.A.S, enabling the incorporation of new features and technologies to meet the changing needs of users
## Desktop Client  
  
The Desktop Client serves as the user's primary interface with K.L.A.A.S, designed for direct interaction with the file system on their computer. Built using PyQt5, it ensures a responsive and visually appealing graphical user interface that operates smoothly across different operating systems. This client enables users to perform a myriad of tasks such as searching for files, organising them into folders, optimising storage through compression and deduplication, and preparing files for sharing. This design emphasises ease of use, aiming to make complex file management tasks accessible to users with varying levels of technical proficiency. It is composed of several key elements:  
  
1. **Search Bar:** A dynamic search utility that allows users to quickly locate files within their local environment. It uses a combination of Qt's QLineEdit for input and QListWidget for displaying real-time search results with custom-styled elements. It is implemented using a custom search algorithm that leverages Python's os library to traverse the file system and the bespoke File System Node Model described below.  
2. **File Management:** This module leverages the Python os and shutil libraries to provide file operations like moving, renaming, deleting, and organising files into folders.  
3. **File Optimisation:** A feature that includes utilities to compress files, remove duplicates, and perform other optimisation tasks to save disk space and enhance organisation.  
4. **Share Functionality:** Integrated within the client, this feature prepares files for sharing by interacting with the Flask Web Server. It packages files, creates shareable links, and communicates with the server via RESTful APIs.  
  
## File System Node / Model Structure  
  
```plaintext  
The data used in this project is from the following sources:  
  
- Data source 1: Local filesystem metadata  
- Data source 2: User input and file operations  
- Data source 3: Cloud storage API for file sharing capabilities  
```  
  
### File System Node Structure  
  
The file system node structure comprises of two main classes that represent the file system hierarchy:  
  
1. **Directory Node:** Represents a directory in the file system. It contains a set of child nodes, which can be either files or subdirectories. The root node is the top-level directory in the file system. Because of this structure, the head node is used to represent the entirety of the file system hierarchy. 
2. **File Node:** Represents a file in the file system. File objects contain useful metadata such as file size, creation date, and file type. It also contains a reference to the parent directory node. The file node is a leaf node in the overall file system node structure.  
  
### File System Cache  
  
The file system cache is the data structure that stores the file system node structure by using the root node. The structure is stored in a pickle (.pkl) file to maintain the state of the head FileSystemNode object in memory. It is used to improve performance by reducing the number of file system accesses and to provide a consistent view of the file system across different parts of the application. The body of the cache is implemented as a dictionary that maps file paths to file system nodes. The cache is updated whenever the file system is modified, ensuring that it remains synchronised with the underlying file system.  
  
## Flask Web Server  
  
At the heart of K.L.A.A.S's sharing functionality is the Flask Web Server, which handles the distribution and management of shared files. Flask was chosen for its lightweight nature and adaptability, allowing for the efficient handling of file transfer requests while maintaining a minimal server footprint. The web server facilitates the secure upload and download of files, employing robust authentication and encryption to safeguard data. The Flask Web Server acts as a file hosting platform to facilitate file sharing:  
  
1. **API Endpoints:** The server provides endpoints for uploading and downloading files. It authenticates requests from the Desktop Client and serves files to external users with temporary access.  
2. **File Hosting:** Temporarily hosts the files shared by the user. It manages a directory where files are stored until they expire.  
3. **Security:** Implements basic security measures to ensure that only authorized users can upload or access files. This may include token-based authentication, HTTPS for secure transmission, and rate-limiting to prevent abuse.  
  
## Expiry Service  

An integral part of the web server is the Expiry Service, which automates the lifecycle management of shared files. This service ensures that files are only available for the duration specified by the user at the time of sharing, after which they are automatically deleted to protect privacy and manage server storage space efficiently. The Expiry Service runs periodic checks on the file repository, identifying and removing files that have reached their expiration date.
The following components are responsible for managing the lifecycle of shared files:  
  
1. **Expiry Mechanism**: It regularly checks the timestamps of hosted files and removes them once their sharing period has expired.  
2. **Cleanup**: Frees up server space by safely deleting expired files and any associated metadata.  

## WebUI Client  
The WebUI Client is a simple web interface that allows external users to access shared files. It is implemented using HTML, CSS, and JavaScript and is served by the Flask Web Server. This component allows recipients of shared files to download them through a secure, temporary link. The WebUI includes features such as a countdown timer to indicate the availability period of the shared files and basic instructions for users to follow for downloading files.

This design ensures that external users do not need to install any special software to access files, making K.L.A.A.S a convenient option for both the sender and the recipient of shared files.
  
## Data Flow  
The architecture ensures smooth communication between the Desktop Client, Flask Web Server, and WebUI Client. The user interacts with the Desktop Client to manage and select files for sharing. Upon initiating a share operation, the file is sent to the Flask Web Server along with metadata, such as the desired expiry time. This is facilitated through RESTful APIs and secure HTTP(S) protocols, which allow for efficient and secure data transfer. The server stores the file and provides a unique URL which the user can share with others.  

The WebUI Client interacts with the server to facilitate file downloads by external users. As external users access the link, the server authenticates the request and serves the file if it has not yet expired. Concurrently, the Expiry Service runs in the background, periodically removing files that have outlived their share duration.

## Technical Challenges and Solutions
The project presented several technical challenges, which were addressed through careful design and implementation. The following are some of the challenges and their solutions:

Challenge 1: File Synchronization Across Devices.
- Solution: 
  - The file system cache was implemented to maintain a consistent view of the file system across different parts of the application. This allowed for improved performance and ensured that the file system state was synchronised across different components.

Challenge 2:

## Performance Considerations
The performance of K.L.A.A.S is a critical consideration, given the potential impact of file system operations and web server interactions on the user experience. The following performance considerations were taken into account during the design and implementation of the system:

## Lessons Learned  
The project provided many opportunities to learn new skills and techniques. The following are some of the lessons learned:  
  
- **Data Structures:** The importance of choosing the right data structures for efficient file system representation and manipulation. This included the use of tree structures to represent the file system hierarchy and caching to improve performance.  
- **Modular Design:** The importance of modular design and separation of concerns in software development. This allowed for easier testing, maintenance, and extensibility.  
- **RESTful APIs:** The benefits of using RESTful APIs for communication between different components of a system. This allowed for a clean and consistent interface between the Desktop Client and the Flask Web Server.  
- **File System Operations:** The intricacies of file system operations and the challenges of managing file metadata. This included handling file paths, file permissions, and file metadata.  
- **Web Server Security:** The importance of implementing security measures in web servers to protect against unauthorised access and abuse. This included token-based authentication, HTTPS, and rate-limiting.  
  
## Future Work  
The project has provided a solid foundation for future work. The following are some of the areas that could be explored in future work:  
- Greater integration with other systems  
- Improved user interface  
- Enhanced security features  
- More advanced file system node structure  
  
## Conclusion  
K.L.A.A.S design philosophy centres on creating a seamless file management and sharing experience for desktop users. By integrating a robust client application with a lightweight web server, K.L.A.A.S achieves a balance between local file organisation and the convenience of web-based file sharing.  
The project has been successful in achieving this goal and has provided a valuable resource for users.  
  
## Acknowledgements  
The group would like to thank the module lecturer for their support and guidance throughout the project.  
  
## References  
- PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/  
- Flask Documentation: https://flask.palletsprojects.com/en/2.0.x/  
- Python os Module Documentation: https://docs.python.org/3/library/os.html  
- Python shutil Module Documentation: https://docs.python.org/3/library/shutil.html 