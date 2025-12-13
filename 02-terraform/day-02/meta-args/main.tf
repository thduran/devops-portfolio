# resource "local_file" "file1" {
#     content = "This is file1 content"
#     filename = "./file1"
#     depends_on = [ 
#         local_file.file2
#      ]
# }

# resource "local_file" "file2" {
#     content = "This is file2 content"
#     filename = "./file2"
# }

# resource "local_file" "file1" {
#     content = "This is the content of file - ${count.index}"
#     filename = "./file${count.index}"
#     count =  4
# }

# resource "local_file" "file1" {
#     content = "This is the content of file - ${count.index + 1}"
#     filename = "./file${count.index + 1}"
#     count =  var.counter
# }

# variable "counter" {
#     default = 10
# }

resource "local_file" "file1" {
    content = "You have to choose: ${each.key}"
    filename = "./file${each.key}.txt"
    for_each = var.foreach
}

variable "foreach" {
    default = ["Machine-01","Machine-02","Machine-03"]
    type = set(string)
}