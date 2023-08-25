from checkers import checkout, getout
import yaml

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)
    arch_format = data['archive_format']

class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files, print_time):
        # test1
        command = f"cd {{}}; 7z a -t{arch_format} {{}}/arx"
        res1 = checkout(command.format(data["folder_in"], data["folder_out"]), "Everything is Ok")
        res2 = checkout("ls {}".format(data["folder_out"]), "arx.7z")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        command1 = f"cd {{}}; 7z a -t{arch_format} {{}}/arx"
        command2 = f"cd {{}}; 7z e arx.{arch_format} -o{{}} -y"
        res.append(checkout(command1.format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        res.append(checkout(command2.format(data["folder_out"], data["folder_ext"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_ext"]), item))
        assert all(res)

    def test_step3(self):
        # test3
        command = f"cd {{}}; 7z t arx.{arch_format}"
        assert checkout(command.format(data["folder_out"]), "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        command = f"cd {{}}; 7z u arx2.{arch_format}"
        assert checkout(command.format(data["folder_in"]), "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        command1 = f"cd {{}}; 7z a -t{arch_format} {{}}/arx"
        command2 = f"cd {{}}; 7z l arx.{arch_format}"
        res.append(checkout(command1.format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        for i in make_files:
            res.append(checkout(command2.format(data["folder_out"], data["folder_ext"]), i))
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        command1 = f"cd {{}}; 7z a -t{arch_format} {{}}/arx"
        command2 = f"cd {{}}; 7z x arx.{arch_format} -o{{}} -y"
        res.append(checkout(command1.format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        res.append(checkout(command2.format(data["folder_out"], data["folder_ext2"]), "Everything is Ok"))
        for i in make_files:
            res.append(checkout("ls {}".format(data["folder_ext2"]), i))
        res.append(checkout("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        # test7
        command = f"cd {{}}; 7z d arx.{arch_format}"
        assert checkout(command.format(data["folder_out"]), "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for i in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], i), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["folder_in"], i)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], i), hash))
        assert all(res), "test8 FAIL"