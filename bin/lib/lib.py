import os
import sys
import subprocess
import platform


def run_it(command, printresult=True):
    if printresult:
        print(" ".join(command))
    p = subprocess.run(command, stdout=subprocess.PIPE)
    r = (p.returncode, p.stdout.decode("ascii").strip("\n"))
    if printresult and r[0] != 0 and r[1] != '':
        print(r)
    return r


class Systemctl:

    def __init__(self, procname):
        self.procname = procname


    def issomething(self, what):
        return run_it(["/bin/systemctl", what, self.procname], printresult=False)


    def isactive(self):
        what = self.issomething("is-active")
        if what == (0, 'active'):
            return True
        elif what == (3, 'inactive'):
            return False
        else:
            raise Exception("isactive", what)


    def isenabled(self):
        what = self.issomething("is-enabled")
        if what == (0, 'enabled'):
            return True
        elif what == (1, 'disabled'):
            return False
        else:
            raise Exception("isenabled", what)


    def isfailed(self):
        return self.issomething("is-failed")


class UwsgiProcess(Systemctl):

    def __init__(self, site, atwhat):
        self.site = site
        self.procname = "uwsgi-" + site + "@" + atwhat
        
        
    def systemctl(self, what):
        run_it(["sudo",
                "-u", self.site,
                "--",
                "/bin/bash", "-c",
                "sudo /bin/systemctl " +  what + " " + self.procname])
        
        
    def start(self):
        self.systemctl("start")
        
        
    def enable(self):
        self.systemctl("enable")
        
        
    def stop(self):
        self.systemctl("stop")

        
    def disable(self):
        self.systemctl("disable")

    
class UwsgiProcesses():

    def __init__(self, site, TEAMS, procname):
        self.site = site
        self.processes = list(map(lambda team:UwsgiProcess(site, team + '.' + procname), TEAMS))


    def systemctl(self, what):
        for s in self.processes:
            s.systemctl(what)


    def start(self):
        self.systemctl("start")


    def enable(self):
        self.systemctl("enable")


    def stop(self):
        self.systemctl("stop")


    def disable(self):
        self.systemctl("disable")


    def areactive(self):
        for p in self.processes:
            if not p.isactive():
                return False
        return True


    def areenabled(self):
        for p in self.processes:
            if not p.isenabled():
                return False
        return True


    def oneactive(self):
        for p in self.processes:
            if p.isactive():
                return True
        return False


    def oneenabled(self):
        for p in self.processes:
            if p.isenabled():
                return True
        return False


class Site:

    def __init__(self, site, TEAMS):
        self.site = site
        self.path = "/home/" + site + "/001"
        self.env = self.path + "/" + site + ".env"
        self.sockets = UwsgiProcesses(site, TEAMS, "socket")
        self.services = UwsgiProcesses(site, TEAMS, "service")


    def run_with_env(self, command):
        run_it(["sudo", "-u", self.site, "--", "/bin/bash", "-c", ". " + self.env + " ; " + command])


    def run_in(self, command):
        run_it(["sudo", "-u", self.site, "--", "/bin/bash", "-c", "cd " + self.path + " ; " + command])


    def start(self):
        self.sockets.enable()
        self.sockets.start()
        self.services.start()
        assert self.sockets.areactive()
        assert self.services.areactive()
        assert self.sockets.areenabled()


    def is_in_test(self):
        return self.sockets.oneactive() or\
            self.services.oneactive() or\
            self.sockets.oneenabled() or\
            os.path.isfile("/etc/nginx/sites-enabled/www-test")

    
    def stop(self):
        # Il est important de stopper la socket et non seulement le service
        # En effet, même arrêté, démarre à la moindre requête d'accès site via la socket
        self.sockets.disable()
        self.sockets.stop()
        self.services.stop()
        assert(not self.is_in_test())

        
    def efface_cms(self):
        self.run_with_env("/home/siteadmin/dju-siteadmin/bin/efface_base.py --oui-efface DJBASE")


    def efface_backend(self):
        self.run_with_env("/home/siteadmin/dju-siteadmin/bin/efface_base.py --oui-efface INTRABASE")


    def reload_cms(self, chemin):
        self.run_with_env("psql $DJBASE < " + chemin)


    def reload_backend(self, chemin):
        self.run_with_env("psql $INTRABASE < " + chemin)


    def rename_sites(self):
        self.run_with_env("/home/siteadmin/dju-siteadmin/bin/rename-sites.py")
        

    def efface_media(self):
        self.run_in("rm -rf media")


    def tar_media(self, chemin):
        self.run_in("/bin/tar xvf " + chemin)


    @classmethod
    def get_test_site(cls, TEAMS):
        f = os.readlink("/etc/nginx/sites-enabled/www")
        if f == "/etc/nginx/sites-available/www-sur-site1":
            site = cls("site2", TEAMS)
        elif f == "/etc/nginx/sites-available/www-sur-site2":
            site = cls("site1", TEAMS)
        else:
            return None
        return site


    def other(self, TEAMS):
        if self.site == "site1":
            return Site("site2", TEAMS)
        elif self.site == "site2":
            return Site("site1", TEAMS)
        else:
            return None


    def test_the_site(self, TEST_URL):
        site = self.site
        p = subprocess.run(["curl", TEST_URL], stdout=subprocess.PIPE)
        if p.returncode != 0:
            return -2
        page = p.stdout.decode("utf-8")
        if '<meta name="google-site-verification" content="HcCeYSnmzrumorrlvEPMt_vf2-vL2OOn4EjUto-IPcU" />' in page:
            return 0
        else:
            return -3


def start_testsite(TEAMS):
    testsite = Site.get_test_site(TEAMS)
    if testsite.is_in_test():
        raise Exception("Cannot start test site, " + testsite.site + " is already in test!!!")
    testsite.efface_backend()
    testsite.reload_backend("/home/backupsite/backup/db_edithbackend_latest.dump")
    testsite.efface_cms()
    testsite.reload_cms("/home/backupsite/backup/db_edithcms_latest.dump")
    testsite.rename_sites()
    testsite.efface_media()
    testsite.tar_media("/home/backupsite/backup/media_edithcms_latest.tgz")
    testsite.tar_media("/home/backupsite/backup/media_edithbackend_latest.tgz")
    testsite.start()
    run_it(["sudo", "/bin/ln", "-sf", "/etc/nginx/sites-available/www-test-sur-" + testsite.site, "/etc/nginx/sites-enabled/www-test"])
    run_it(["sudo", "/bin/systemctl", "restart",  "nginx"] )
    return testsite


def start_test(TEAMS):
    testsite = start_testsite(TEAMS)
    print("OK, please use " + testsite.site + " as test site") 


def nginx_stop_www_test():
    run_it(["sudo", "/bin/rm", "/etc/nginx/sites-enabled/www-test"])
    run_it(["sudo", "/bin/systemctl", "restart",  "nginx"])


def stop_test(TEAMS):
    testsite = Site.get_test_site(TEAMS)
    if not testsite.is_in_test():
        raise Exception("Site " + testsite.site + " is not in test !!!")
    nginx_stop_www_test()
    testsite.stop()   


def swap_site(TEAMS, TEST_URL):
    testsite = Site.get_test_site(TEAMS)
    t = testsite.test_the_site(TEST_URL)
    if t != 0:
        raise Exception("Bad test site, swap operation is aborted!!!")
    run_it(["sudo", "/bin/ln", "-sf", "/etc/nginx/sites-available/www-sur-" + testsite.site, "/etc/nginx/sites-enabled/www"])
    nginx_stop_www_test()
    testsite.other(TEAMS).stop()


def migrate_data(TEAMS, TEST_URL):
    testsite = start_testsite(TEAMS)
    swap_site(TEAMS, TEST_URL)
