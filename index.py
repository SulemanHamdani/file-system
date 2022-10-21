from lib import File, Folder

# Data initializaion
root = Folder("~")
images = Folder("images")

suleman = File("suleman.txt", '~/images/')
farhan = File("farhan.txt", '~/images/')
suleman.update_content('suleman')
farhan.update_content('farhan')

root.add(images)
images.add(farhan)
images.add(suleman)

print(len(root.children))
print(len(images.children))