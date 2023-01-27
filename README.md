## JSONL to UIMA CAS XMI 1.0 Converter

This excerise provides a tool for converting a JSONL file to UIMA CAS XMI 1.0 format. This format can be used on INCEpTION, an open-source platform for creating, running, and evaluating natural language processing (NLP) systems.

### Getting Started
To use this tool, you will need to have the following installed on your system:
- Python 3.6 or later

Once you have these dependencies installed, you can download the latest release of the JSONL to UIMA CAS XMI 1.0 Converter from the releases page of this repository.

### Usage
To convert a JSONL file to UIMA CAS XMI 1.0 format, you can use the following command:

```python
python converter.py <input-file.xml> <input-file.jsonl> <result-path>
```

Where `<input-file.jsonl>` is the path to the JSONL file you want to convert, and `<descriptor-file.xml>` is the path to the custom descriptor file. `<result-path>` is set defult to current folder.

### Example
Let's say you have a JSONL file called `example.jsonl` in the same directory as the converter. To convert this file to XMI format, you would use the following command:

```python
python converter.py example.xml example.jsonl
```
This would create an XMI file called `example.xmi` in the same directory as the input file.

### Support
If you have any issues or questions about this tool, please open an issue in this repository or contact the author directly.
