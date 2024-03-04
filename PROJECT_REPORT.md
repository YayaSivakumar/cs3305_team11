# CS3305 Group 11 - PROJECT REPORT
## Project Title - File Organizer, Explorer and Sharing System

## Introduction

Our application, File Explorer, Organiser and Sharing (FEOS), is designed to streamline the user's interaction with their local filesystem and enhance file management, sharing, and optimization. It allows users to not only manage their files locally but also to share them via a built-in web server powered by Flask, a lightweight WSGI web application framework.

## Project Objectives

The objectives of the project are as follows:

1. To develop a unified platform that simplifies file management through automatic sorting, in-depth organization, and scheduling features.
2. To enable efficient file sharing capabilities through a cloud-based system, allowing users to share files with external parties securely.
3. To implement advanced file optimization techniques such as compression and deduplication, thereby enhancing storage efficiency and organization.

## Architecture

The architecture of FEOS is modular, consisting of three primary components: the Desktop Client, the Flask Web Server(including the Expiry Service), and the WebUI client.

## Desktop Client

The Desktop Client is the heart of FEOS, implemented using PyQt5 to provide a cross-platform graphical user interface (GUI). It is composed of several key elements:

1. **Search Bar:** A dynamic search utility that allows users to quickly locate files within their local environment. It uses a combination of Qt's QLineEdit for input and QListWidget for displaying real-time search results with custom-styled elements. It is implemented using a custom search algorithm that leverages Python's os library to traverse the file system and the bespoke File System Node Model described below.
2. **File Management:** This module leverages the Python os and shutil libraries to provide file operations like moving, renaming, deleting, and organizing files into folders.
3. **File Optimization:** A feature that includes utilities to compress files, remove duplicates, and perform other optimization tasks to save disk space and enhance organization.
3. **Share Functionality:** Integrated within the client, this feature prepares files for sharing by interacting with the Flask Web Server. It packages files, creates shareable links, and communicates with the server via RESTful APIs.

## File System Node / Model Structure

```plaintext
The data used in this project is from the following sources:

- Data source 1: Local filesystem metadata
- Data source 2: User input and file operations
- Data source 3: Cloud storage API for file sharing capabilities
```

### File System Node Structure

The file system node structure defines two main classes that represent the file system hierarchy:

1. **Directory Node:** Represents a directory in the file system. It contains a list of child nodes, which can be either files or subdirectories. The root node is the top-level directory in the file system. It contains a list of child nodes, which can be either files or subdirectories. The head of the file system node structure is the root node. It is used to represent the entire file system hierarchy.
2. **File Node:** Represents a file in the file system. It contains metadata such as file size, creation date, and file type. It also contains a reference to the parent directory node. The file node is a leaf node in the file system node structure. 

### File System Cache

The file system cache is the data structure that stores the file system node structure by using the root node. The structure is stored in a pickle (.pkl) file to maintain the state of the head FileSystemNode object in memory. It is used to improve performance by reducing the number of file system accesses and to provide a consistent view of the file system across different parts of the application. The body of the cache is implemented as a dictionary that maps file paths to file system nodes. The cache is updated whenever the file system is modified, ensuring that it remains synchronized with the underlying file system. 

## Flask Web Server

The Flask Web Server acts as a file hosting platform to facilitate file sharing:

1. **API Endpoints:** The server provides endpoints for uploading and downloading files. It authenticates requests from the Desktop Client and serves files to external users with temporary access.
2. **File Hosting:** Temporarily hosts the files shared by the user. It manages a directory where files are stored until they expire.
3. **Security:** Implements basic security measures to ensure that only authorized users can upload or access files. This may include token-based authentication, HTTPS for secure transmission, and rate-limiting to prevent abuse.

## Expiry Service
This component is responsible for managing the lifecycle of shared files:

1. **Expiry Mechanism**: It regularly checks the timestamps of hosted files and removes them once their sharing period has expired.
2. **Cleanup**: Frees up server space by safely deleting expired files and any associated metadata.


## WebUI Client
The WebUI Client is a simple web interface that allows external users to access shared files. It is implemented using HTML, CSS, and JavaScript and is served by the Flask Web Server. It provides a basic user interface for downloading shared files and includes a countdown timer to indicate the remaining time before the file expires.


## Data Flow
The user interacts with the Desktop Client to manage and select files for sharing. Upon initiating a share operation, the file is sent to the Flask Web Server along with metadata, such as the desired expiry time. The server stores the file and provides a unique URL which the user can share with others.
As external users access the link, the server authenticates the request and serves the file if it has not yet expired. Concurrently, the Expiry Service runs in the background, periodically removing files that have outlived their share duration.

## Lessons Learned
The project provided many opportunities to learn new skills and techniques. The following are some of the lessons learned:

- **Data Structures:** The importance of choosing the right data structures for efficient file system representation and manipulation. This included the use of tree structures to represent the file system hierarchy and caching to improve performance.
- **Modular Design:** The importance of modular design and separation of concerns in software development. This allowed for easier testing, maintenance, and extensibility. 
- **RESTful APIs:** The benefits of using RESTful APIs for communication between different components of a system. This allowed for a clean and consistent interface between the Desktop Client and the Flask Web Server.
- **File System Operations:** The intricacies of file system operations and the challenges of managing file metadata. This included handling file paths, file permissions, and file metadata.
- **Web Server Security:** The importance of implementing security measures in web servers to protect against unauthorized access and abuse. This included token-based authentication, HTTPS, and rate-limiting.

## Future Work
The project has provided a solid foundation for future work. The following are some of the areas that could be explored in future work:
- Greater integration with other systems
- Improved user interface
- Enhanced security features
- More advanced file system node structure

## Conclusion
FEOS design philosophy centers on creating a seamless file management and sharing experience for desktop users. By integrating a robust client application with a lightweight web server, FEOS achieves a balance between local file organization and the convenience of web-based file sharing.
The project has been successful in achieving this goal and has provided a valuable resource for users.

## Acknowledgements
The group would like to thank the module lecturer for their support and guidance throughout the project. 

## References
- PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/
- Flask Documentation: https://flask.palletsprojects.com/en/2.0.x/
- Python os Module Documentation: https://docs.python.org/3/library/os.html
- Python shutil Module Documentation: https://docs.python.org/3/library/shutil.html

In conclusion, the project has been a valuable learning experience and has provided a solid foundation for future work in the area of file management and sharing systems. The team has worked well together and has produced a high-quality product that meets the objectives set out at the beginning of the project. The team looks forward to further developing and refining the system in the future.