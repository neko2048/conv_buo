import sys, os

def check_folder(fig_dir):
    parent_folders = fig_dir.split('/')
    case_name = parent_folders[-4]
    type_name = parent_folders[-3]
    var_name = parent_folders[-2]
    if not os.path.isdir(fig_dir):
        print("No {CN}/{TN}/{VN} Folder, Creating..."\
              .format(CN=case_name, 
                      TN=type_name,
                      VN=var_name))
        os.mkdir(fig_dir)