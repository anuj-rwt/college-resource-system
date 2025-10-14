import datetime

class FileNode:
    def __init__(self, filename, resource_type, course, year, semester, exam_type, filepath):
        self.filename = filename
        self.resource_type = resource_type
        self.course = course
        self.year = year
        self.semester = semester
        self.exam_type = exam_type
        self.filepath = filepath
        self.upload_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.next = None


class FileLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, filename, resource_type, course, year, semester, exam_type, filepath):
        """Insert new file node at the end"""
        new_node = FileNode(filename, resource_type, course, year, semester, exam_type, filepath)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def filter_files(self, **kwargs):
        """Filter files based on hierarchy"""
        results = []
        temp = self.head
        while temp:
            match = True
            for key, value in kwargs.items():
                if getattr(temp, key) != value:
                    match = False
                    break
            if match:
                results.append(temp)
            temp = temp.next
        return results
