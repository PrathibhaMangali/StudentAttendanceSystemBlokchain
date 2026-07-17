pragma solidity >= 0.8.11 <= 0.8.11;
pragma experimental ABIEncoderV2;
//Attendance solidity code
contract Attendance {

    uint public studentCount = 0; 
    mapping(uint => student) public studentList; 
     struct student
     {
       string studentid;
       string name;
       string course;
       string phone;
       string email;
       string student_address;
     }
 
   // events 
   event studentCreated(uint indexed _userId);
   
   //function  to save student details to Blockchain
   function saveStudent(string memory sid, string memory std_name, string memory std_course, string memory std_phone, string memory std_email, string memory std_address) public {
      studentList[studentCount] = student(sid, std_name, std_course, std_phone, std_email, std_address);
      emit studentCreated(studentCount);
      studentCount++;
    }

     //get student count
    function getStudentCount()  public view returns (uint) {
          return  studentCount;
    }

    uint public attendanceCount = 0; 
    mapping(uint => attendance) public attendanceList; 
     struct attendance
     {
       string studentId;
       string attendance_date;
       string class_name;       
     }
 
   // events 
   event attendanceCreated(uint indexed _iotId);
   
   //function  to save attendance data to Blockchain
   function saveAttendance(string memory sid, string memory sdate, string memory cname) public {
      attendanceList[attendanceCount] = attendance(sid, sdate, cname);
      emit attendanceCreated(attendanceCount);
      attendanceCount++;
    }

    //get attendance count
    function getAttendanceCount()  public view returns (uint) {
          return attendanceCount;
    }

    function getStdID(uint i) public view returns (string memory) {
        attendance memory doc = attendanceList[i];
	return doc.studentId;
    }

    function getAttendanceDate(uint i) public view returns (string memory) {
        attendance memory doc = attendanceList[i];
	return doc.attendance_date;
    }

    function getClassName(uint i) public view returns (string memory) {
        attendance memory doc = attendanceList[i];
	return doc.class_name;
    }    

    function getEmail(uint i) public view returns (string memory) {
        student memory doc = studentList[i];
	return doc.email;
    }

    function getAddress(uint i) public view returns (string memory) {
        student memory doc = studentList[i];
	return doc.student_address;
    }

    function getID(uint i) public view returns (string memory) {
        student memory doc = studentList[i];
	return doc.studentid;
    }

    function getPhone(uint i) public view returns (string memory) {
        student memory doc = studentList[i];
	return doc.phone;
    }

    function getName(uint i) public view returns (string memory) {
        student memory doc =studentList[i];
	return doc.name;
    }

    function getCourse(uint i) public view returns (string memory) {
        student memory doc =studentList[i];
	return doc.course;
    }
        
}