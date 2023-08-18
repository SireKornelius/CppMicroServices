# Python Command Line Utility for Customizing CppMicroServices Namespace

This is a Python command line utility that allows you to customize the namespace of the CppMicroServices library.
## Prerequisites

- Python 3.5+
- CppMicroServices library source code

## Installation

1. Clone the repository or download the source code.
2. No additional Python dependencies are required.

## Usage

To customize the namespace of the CppMicroServices library and build it in a new directory, follow these steps:

1. Obtain the source code of the CppMicroServices library.
2. Run the command line utility with the following command on Windows (python3 on Linux and macOS):

   ```
   python <path_to_script> <new_namespace> <path_to_new_dir>
   ```

   - Replace `<path_to_script>` with the path to the script file. If cwd is set to CppMicroServices directory the relative path would be ./tools/customNS/src/script.py.
   - Replace `<new_namespace>` with the desired new namespace.
   - Replace `<path_to_new_dir>` with the path to the directory where the modified library will be built.

3. The utility will copy the necessary files from the CppMicroServices library to the specified new directory, modifying the namespace to the provided new namespace.

4. Navigate to the new directory and build the modified CppMicroServices library.
## Example

Suppose you have obtained the source code of the CppMicroServices library and it is located at `/path/to/CppMicroServices`. To customize the namespace to `mw_cppms` and build the modified library in `/path/to/new_dir`, run the following command:

```
python /path/to/CppMicroServices/tools/customNS/src/script.py mw_cppms /path/to/new_dir
```

The utility will copy the necessary files from the CppMicroServices library to `/path/to/new_dir`, modifying the namespace to `my_custom_namespace`. Then, navigate to `/path/to/new_dir` and build the modified CppMicroServices library.

## Limitations
1. No support for changing namespace to consist of non-english characters even if it may be valid C++ syntax
2. Documentation will not be modified

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request.

## Contact

For any questions or inquiries, please contact kjiamsri@mathworks.com.