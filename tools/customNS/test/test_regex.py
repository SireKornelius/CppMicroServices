import unittest
from src.utils import NamespaceModifier
""" All usages of namespaces according to cppreferences

namespace ns-name { declarations }	(1)	
inline namespace ns-name { declarations }	(2)	(since C++11)
namespace { declarations }	(3)
ns-name :: member-name	(4)	
using namespace ns-name ;	(5)	
using ns-name :: member-name ;	(6)	
namespace name = qualified-namespace ;	(7)	
namespace ns-name :: member-name { declarations }	(8)	(since C++17)
namespace ns-name :: inline member-name { declarations }	(9)	(since C++20)
"""
class TestRegex(unittest.TestCase):

    def test_match_reg_name_dec(self):
        """
        Should match (1) (2) (5) (/8) (/9)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        #match (1)
        self.assertEqual(
            ("namespace mw_cppms {}", 1), 
            ns_test.reg_name_dec("namespace cppmicroservices {}")
            )
        self.assertEqual(
            ("namespace mw_cppms", 1),
            ns_test.reg_name_dec("namespace cppmicroservices")
            )
        self.assertEqual(
            (" namespace mw_cppms {}", 1), 
            ns_test.reg_name_dec(" namespace cppmicroservices {}")
            )
        self.assertEqual(
            (" namespace  mw_cppms  {}", 1), 
            ns_test.reg_name_dec(" namespace  cppmicroservices  {}")
            )
        self.assertEqual(
            ("namespace mw_cppms ", 1), 
            ns_test.reg_name_dec("namespace cppmicroservices ")
            )
        self.assertEqual(
            ("  namespace   mw_cppms   {", 1), 
            ns_test.reg_name_dec("  namespace   cppmicroservices   {")
            )
        self.assertEqual(
            ('"namespace mw_cppms"', 1), 
            ns_test.reg_name_dec('"namespace cppmicroservices"')
            )
        self.assertEqual(
            ('("namespace mw_cppms")', 1), 
            ns_test.reg_name_dec('("namespace cppmicroservices")')
            )
        self.assertEqual(
            ("namespace mw_cppms { namespace mw_cppms }", 2), 
            ns_test.reg_name_dec("namespace cppmicroservices { namespace cppmicroservices }")
            )
        self.assertEqual(
            ("namespace\n mw_cppms", 1), 
            ns_test.reg_name_dec("namespace\n cppmicroservices")
            )
        self.assertEqual(
            ("namespace\n\n  mw_cppms", 1), 
            ns_test.reg_name_dec("namespace\n\n  cppmicroservices")
            )
        self.assertEqual(
            ("namespace  \n \n  mw_cppms", 1), 
            ns_test.reg_name_dec("namespace  \n \n  cppmicroservices")
            )
        self.assertEqual(
            ("namespace \n\t mw_cppms", 1), 
            ns_test.reg_name_dec("namespace \n\t cppmicroservices")
            )
        self.assertEqual(
            ("namespace \r\n mw_cppms", 1), 
            ns_test.reg_name_dec("namespace \r\n cppmicroservices")
            )
        self.assertEqual(
            ('"namespace" "mw_cppms"', 1), 
            ns_test.reg_name_dec('"namespace" "cppmicroservices"')
            )
        self.assertEqual(
            ('"namespace" \n\n"mw_cppms"', 1), 
            ns_test.reg_name_dec('"namespace" \n\n"cppmicroservices"')
            )

        # match (2)
        self.assertEqual(
            ("inline namespace mw_cppms", 1), 
            ns_test.reg_name_dec("inline namespace cppmicroservices")
            )

        # match (5)
        self.assertEqual(
            ("using namespace mw_cppms", 1), 
            ns_test.reg_name_dec("using namespace cppmicroservices")
            )
        self.assertEqual(
            (" using   namespace   mw_cppms", 1), 
            ns_test.reg_name_dec(" using   namespace   cppmicroservices")
            )
        self.assertEqual(
            ("using namespace mw_cppms;", 1), 
            ns_test.reg_name_dec("using namespace cppmicroservices;")
            )
        self.assertEqual(
            ("using namespace mw_cppms ;", 1), 
            ns_test.reg_name_dec("using namespace cppmicroservices ;")
            )
        self.assertEqual(
            ("using\nnamespace mw_cppms", 1), 
            ns_test.reg_name_dec("using\nnamespace cppmicroservices")
            )
        self.assertEqual(
            ("using\nnamespace \nmw_cppms", 1), 
            ns_test.reg_name_dec("using\nnamespace \ncppmicroservices")
            )
        self.assertEqual(
            ("using\nnamespace \t\n mw_cppms;", 1), 
            ns_test.reg_name_dec("using\nnamespace \t\n cppmicroservices;")
            )
        # match (/8)
        self.assertEqual(
            ("namespace mw_cppms::test {}", 1), 
            ns_test.reg_name_dec("namespace cppmicroservices::test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms:: test {}", 1), 
            ns_test.reg_name_dec("namespace cppmicroservices:: test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms :: test {}", 1), 
            ns_test.reg_name_dec("namespace cppmicroservices :: test {}")
            )
        self.assertEqual(
            ("namespace \nmw_cppms\n::\ntest {}", 1), 
            ns_test.reg_name_dec("namespace \ncppmicroservices\n::\ntest {}")
            )
        self.assertEqual(
            ("namespace \nmw_cppms\n ::test {}", 1), 
            ns_test.reg_name_dec("namespace \ncppmicroservices\n ::test {}")
            )

        # match (/9)
        self.assertEqual(
            ("namespace mw_cppms::inline test{}", 1), 
            ns_test.reg_name_dec("namespace cppmicroservices::inline test{}")
            )
        self.assertEqual(
            ("namespace mw_cppms:: inline test {}", 1), 
            ns_test.reg_name_dec("namespace cppmicroservices:: inline test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms :: inline test {}", 1), 
            ns_test.reg_name_dec("namespace cppmicroservices :: inline test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms::\ninline test {}", 1), 
            ns_test.reg_name_dec("namespace cppmicroservices::\ninline test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms::\ninline\ntest {}", 1), 
            ns_test.reg_name_dec("namespace cppmicroservices::\ninline\ntest {}")
            )
        self.assertEqual(
            ("namespace\nmw_cppms::\ninline test {}", 1), 
            ns_test.reg_name_dec("namespace\ncppmicroservices::\ninline test {}")
            )


    def test_not_match_reg_name_dec(self): 
        """
        Should not match (1) (2) (5) (/8) (/9)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        # not match (1)
        self.assertEqual(
            ("int temp = 3",0), 
            ns_test.reg_name_dec("int temp = 3")
            )
        self.assertEqual( 
            ("std::vector<BundleResource> schemeResources = GetBundleContext().GetBundle().FindResources(\"/\", \"*.scm\", false);",0), 
            ns_test.reg_name_dec("std::vector<BundleResource> schemeResources = GetBundleContext().GetBundle().FindResources(\"/\", \"*.scm\", false);")
            )

        self.assertEqual(
            ("namespace", 0), 
            ns_test.reg_name_dec("namespace")
            )
        self.assertEqual(
            ("cppmicroservices", 0), 
            ns_test.reg_name_dec("cppmicroservices")
            )
        self.assertEqual(
            ("namespace Cppmicroservices", 0), 
            ns_test.reg_name_dec("namespace Cppmicroservices")
            )  
        self.assertEqual(
            ("code::something::namespace::cppmicroservices", 0), 
            ns_test.reg_name_dec("code::something::namespace::cppmicroservices")
            )
        self.assertEqual(
            ("namespace notcppmicroservices", 0), 
            ns_test.reg_name_dec("namespace notcppmicroservices")
            )
        self.assertEqual(
            ("namespace acppmicroservicesb", 0), 
            ns_test.reg_name_dec("namespace acppmicroservicesb")
            )
        self.assertEqual(
            ("anamespace cppmicroservices", 0), 
            ns_test.reg_name_dec("anamespace cppmicroservices")
            ) 
        self.assertEqual(
            ("namespace cppmicroservicess", 0), 
            ns_test.reg_name_dec("namespace cppmicroservicess")
            )
        self.assertEqual(
            ("namespace\ncppmicroservicess", 0), 
            ns_test.reg_name_dec("namespace\ncppmicroservicess")
            )
        self.assertEqual(
            (" namespace\n\n cppmicroservicess { }", 0), 
            ns_test.reg_name_dec(" namespace\n\n cppmicroservicess { }")
            )
        self.assertEqual(
            ("namespace\n\tcppmicroservicess", 0), 
            ns_test.reg_name_dec("namespace\n\tcppmicroservicess")
            )
        
        # not match (2)       
        self.assertEqual(
            ("inline namespace cppmicroservicess", 0), 
            ns_test.reg_name_dec("inline namespace cppmicroservicess")
            )
        self.assertEqual(
            ("inline namespace\nCppmicroservices", 0), 
            ns_test.reg_name_dec("inline namespace\nCppmicroservices")
            )
        self.assertEqual(
            ("inline\nnamespace\n\tCppmicroservices", 0), 
            ns_test.reg_name_dec("inline\nnamespace\n\tCppmicroservices")
            )
        # not match (5)
        self.assertEqual(
            ("using namespace cppmicroservicess;", 0), 
            ns_test.reg_name_dec("using namespace cppmicroservicess;")
            )
        self.assertEqual(
            ("using namespace Cppmicroservices", 0), 
            ns_test.reg_name_dec("using namespace Cppmicroservices")
            )
        self.assertEqual(
            ("using namespace\ncppmicroservicess;", 0), 
            ns_test.reg_name_dec("using namespace\ncppmicroservicess;")
            )
        self.assertEqual(
            ("using\nnamespace\n\nCppmicroservices", 0), 
            ns_test.reg_name_dec("using\nnamespace\n\nCppmicroservices")
            )
        # not match (8)
        self.assertEqual(
            ("namespace top_namespace::test {}", 0), 
            ns_test.reg_name_dec("namespace top_namespace::test {}")
            )
        self.assertEqual(
            ("namespace\ntop_namespace::test {}", 0), 
            ns_test.reg_name_dec("namespace\ntop_namespace::test {}")
            )
        # not match (9)
        self.assertEqual(
            ("namespace top_namespace::inline test {}", 0), 
            ns_test.reg_name_dec("namespace top_namespace::inline test {}")
            )
        self.assertEqual(
            ("namespace\ntop_namespace::inline test {}", 0), 
            ns_test.reg_name_dec("namespace\ntop_namespace::inline test {}")
            )


    def test_match_reg_alias_name(self):
        """
        Should match (7)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        # match (7)
        self.assertEqual(
            ("namespace something = mw_cppms", 1), 
            ns_test.reg_alias_name("namespace something = cppmicroservices")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  mw_cppms ", 1), 
            ns_test.reg_alias_name(" namespace  somethingelse  =  cppmicroservices ")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  mw_cppms; ", 1), 
            ns_test.reg_alias_name(" namespace  somethingelse  =  cppmicroservices; ")
            )

        self.assertEqual(
            ("namespace something =\n mw_cppms", 1), 
            ns_test.reg_alias_name("namespace something =\n cppmicroservices")
            )
        self.assertEqual(
            (" namespace  somethingelse  \n=  mw_cppms ", 1), 
            ns_test.reg_alias_name(" namespace  somethingelse  \n=  cppmicroservices ")
            )
        self.assertEqual(
            (" namespace  \nsomethingelse  \n=\n  mw_cppms ", 1), 
            ns_test.reg_alias_name(" namespace  \nsomethingelse  \n=\n  cppmicroservices ")
            )
        self.assertEqual(
            (" namespace\n\tsomethingelse  =  mw_cppms; ", 1), 
            ns_test.reg_alias_name(" namespace\n\tsomethingelse  =  cppmicroservices; ")
            )
        self.assertEqual(
            ('" namespace\n\tsomethingelse" \n=  "mw_cppms; "', 1), 
            ns_test.reg_alias_name('" namespace\n\tsomethingelse" \n=  "cppmicroservices; "')
            )


    def test_not_match_reg_alias_name(self):
        """
        Should not match (7)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        self.assertEqual(
            ("cppmicroservices", 0), 
            ns_test.reg_alias_name("cppmicroservices")
            )
        self.assertEqual(
            ("namespace test = some_namespace", 0), 
            ns_test.reg_alias_name("namespace test = some_namespace")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  cppmicroservicess", 0), 
            ns_test.reg_alias_name(" namespace  somethingelse  =  cppmicroservicess")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  Cppmicroservices", 0), 
            ns_test.reg_alias_name(" namespace  somethingelse  =  Cppmicroservices")
            )
        self.assertEqual(
            (" namespace  somethingelse  \n=\n Cppmicroservices", 0), 
            ns_test.reg_alias_name(" namespace  somethingelse  \n=\n Cppmicroservices")
            )
        self.assertEqual(
            (" namespace\nsomethingelse  \n=\n  Cppmicroservices", 0), 
            ns_test.reg_alias_name(" namespace\nsomethingelse  \n=\n  Cppmicroservices")
            )
        self.assertEqual(
            ("anamespace test = cppmicroservices", 0), 
            ns_test.reg_alias_name("anamespace test = cppmicroservices")
            )

    def test_match_reg_scope_post(self):
        """
        Should match (4) (6)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        # match (4)
        self.assertEqual(
            ("mw_cppms::something", 1), 
            ns_test.reg_scope_post("cppmicroservices::something")
            )
        self.assertEqual(
            ("mw_cppms:: something", 1), 
            ns_test.reg_scope_post("cppmicroservices:: something")
            )
        self.assertEqual(
            ("mw_cppms ::  something", 1), 
            ns_test.reg_scope_post("cppmicroservices ::  something")
            )
        self.assertEqual(
            ("mw_cppms::something::inner", 1), 
            ns_test.reg_scope_post("cppmicroservices::something::inner")
            )
        self.assertEqual(
            ("std::pair<mw_cppms::blah, mw_cppms::smth> var_", 2), 
            ns_test.reg_scope_post("std::pair<cppmicroservices::blah, cppmicroservices::smth> var_")
            )
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ = getSomething(\"mw_cppms::res\")", 2), 
            ns_test.reg_scope_post("std::vector<cppmicroservices::things> var_ = getSomething(\"cppmicroservices::res\")")
            )
        
        self.assertEqual(
            ("mw_cppms::\n\nsomething", 1), 
            ns_test.reg_scope_post("cppmicroservices::\n\nsomething")
            )
        self.assertEqual(
            ("mw_cppms\n:: \nsomething", 1), 
            ns_test.reg_scope_post("cppmicroservices\n:: \nsomething")
            )
        self.assertEqual(
            ("mw_cppms :: \n\tsomething", 1), 
            ns_test.reg_scope_post("cppmicroservices :: \n\tsomething")
            )
        self.assertEqual(
            ("mw_cppms::\nsomething::\ninner", 1), 
            ns_test.reg_scope_post("cppmicroservices::\nsomething::\ninner")
            )
        self.assertEqual(
            ("std::pair<mw_cppms::blah,\nmw_cppms::smth> var_", 2), 
            ns_test.reg_scope_post("std::pair<cppmicroservices::blah,\ncppmicroservices::smth> var_")
            )
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms::res\")", 2), 
            ns_test.reg_scope_post("std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices::res\")")
            )
        
        self.assertEqual(
            ("mw_cppms:: here mw_cppms::there mw_cppms::any", 3), 
            ns_test.reg_scope_post("cppmicroservices:: here cppmicroservices::there cppmicroservices::any")
            )
        self.assertEqual(
            ("mw_cppms::here; mw_cppms::there; mw_cppms::any", 3), 
            ns_test.reg_scope_post("cppmicroservices::here; cppmicroservices::there; cppmicroservices::any")
            )

        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms\"\"::res\")", 2), 
            ns_test.reg_scope_post("std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices\"\"::res\")")
            )
        self.assertEqual( 
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms\"\n\"::res\")", 2), 
            ns_test.reg_scope_post("std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices\"\n\"::res\")")
            )
        # match (6)
        self.assertEqual(
            ("using mw_cppms::some_class", 1), 
            ns_test.reg_scope_post("using cppmicroservices::some_class")
            )
        self.assertEqual(
            ("using mw_cppms::some_class;", 1), 
            ns_test.reg_scope_post("using cppmicroservices::some_class;")
            )
        self.assertEqual(
            ("using mw_cppms:: some_class", 1), 
            ns_test.reg_scope_post("using cppmicroservices:: some_class")
            )
        self.assertEqual(
            ("using mw_cppms::ns::something", 1), 
            ns_test.reg_scope_post("using cppmicroservices::ns::something")
            )
        
        self.assertEqual(
            ("using mw_cppms::\nsome_class", 1), 
            ns_test.reg_scope_post("using cppmicroservices::\nsome_class")
            )
        self.assertEqual(
            ("using\nmw_cppms\n::\nsome_class;", 1), 
            ns_test.reg_scope_post("using\ncppmicroservices\n::\nsome_class;")
            )
        self.assertEqual(
            ("using mw_cppms::\n\t some_class", 1), 
            ns_test.reg_scope_post("using cppmicroservices::\n\t some_class")
            )
        self.assertEqual(
            ("using mw_cppms::\nns::\nsomething", 1), 
            ns_test.reg_scope_post("using cppmicroservices::\nns::\nsomething")
            )


    def test_not_match_reg_scope_post(self):
        """
        Should not match (4) (6)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        # not match (4)
        self.assertEqual(
            ("int temp = 3", 0), 
            ns_test.reg_scope_post("int temp = 3")
            )
        self.assertEqual(
            ("<cppmicroservices>", 0), 
            ns_test.reg_scope_post("<cppmicroservices>")
            )
        self.assertEqual(
            ("cppmicroservices", 0), 
            ns_test.reg_scope_post("cppmicroservices")
            )
        self.assertEqual(
            ("ccppmicroservices::something", 0), 
            ns_test.reg_scope_post("ccppmicroservices::something")
            )
        self.assertEqual(
            ("cppmicroservicess::\nsomething", 0), 
            ns_test.reg_scope_post("cppmicroservicess::\nsomething")
            )
        self.assertEqual(
            ("cppmicroservicess::\n\nsomething", 0), 
            ns_test.reg_scope_post("cppmicroservicess::\n\nsomething")
            )
        self.assertEqual(
            ("cppmicroservicess::\n\n\tsomething", 0), 
            ns_test.reg_scope_post("cppmicroservicess::\n\n\tsomething")
            )
        self.assertEqual(
            ("cppmicroservices'::something", 0), 
            ns_test.reg_scope_post("cppmicroservices'::something")
            )
        self.assertEqual(
            ("Cppmicroservices::something", 0), 
            ns_test.reg_scope_post("Cppmicroservices::something"))

        # not match (6)
        self.assertEqual(
            ("using ns::some_class", 0), 
            ns_test.reg_scope_post("using ns::some_class")
            )
        self.assertEqual(
            ("using ccppmicroservices::thing", 0), 
            ns_test.reg_scope_post("using ccppmicroservices::thing")
            ) 
        self.assertEqual(
            ("using Cppmicroservices::thing", 0), 
            ns_test.reg_scope_post("using Cppmicroservices::thing")
            )     

        self.assertEqual(
            ("using\nns::some_class", 0), 
            ns_test.reg_scope_post("using\nns::some_class")
            )
        self.assertEqual(
            ("using ccppmicroservices\n::thing", 0), 
            ns_test.reg_scope_post("using ccppmicroservices\n::thing")
            ) 
        self.assertEqual(
            ("using\nCppmicroservices\n::\nthing", 0), 
            ns_test.reg_scope_post("using\nCppmicroservices\n::\nthing")
            )       


    def test_match_reg_scope_pre(self):
        """
        Match edge cases (/8) (/9)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        self.assertEqual(
            ("namespace foo::inline mw_cppms{}", 1), 
            ns_test.reg_scope_pre("namespace foo::inline cppmicroservices{}")
            )  
        self.assertEqual(
            ("namespace foo:: \ninline mw_cppms{}", 1), 
            ns_test.reg_scope_pre("namespace foo:: \ninline cppmicroservices{}")
            )   
        self.assertEqual(
            ("namespace foo::mw_cppms{}", 1), 
            ns_test.reg_scope_pre("namespace foo::cppmicroservices{}")
            )  
        self.assertEqual(
            ("namespace foo::\nmw_cppms{}", 1), 
            ns_test.reg_scope_pre("namespace foo::\ncppmicroservices{}")
            )  
        self.assertEqual(
            ("using namespace ::mw_cppms", 1), 
            ns_test.reg_scope_pre("using namespace ::cppmicroservices")
            )  
        self.assertEqual(
            ("using namespace ::\nmw_cppms", 1), 
            ns_test.reg_scope_pre("using namespace ::\ncppmicroservices")
            )  
        self.assertEqual(
            ('"using namespace ::mw_cppms"', 1), 
            ns_test.reg_scope_pre('"using namespace ::cppmicroservices"')
            )   
        self.assertEqual(
            ("using   ::mw_cppms", 1), 
            ns_test.reg_scope_pre("using   ::cppmicroservices")
            )
        self.assertEqual(
            ('"using" "::mw_cppms"', 1), 
            ns_test.reg_scope_pre('"using" "::cppmicroservices"')
            )       
        self.assertEqual(
            ("::mw_cppms", 1), 
            ns_test.reg_scope_pre("::cppmicroservices")
            )    
        self.assertEqual(
            (":: mw_cppms", 1), 
            ns_test.reg_scope_pre(":: cppmicroservices")
            )
        self.assertEqual(
            ("::mw_cppms", 1), 
            ns_test.reg_scope_pre("::cppmicroservices")
            )

    def test_not_match_reg_scope_pre(self):
        """
        Not match edge cases (/8) (/9)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        self.assertEqual(
            ("cppmicroservices", 0), 
            ns_test.reg_scope_pre("cppmicroservices")
            )
        self.assertEqual(
            ("random::something()", 0),
            ns_test.reg_scope_pre("random::something()")
            )
        self.assertEqual(
            ("::cppmicroservicesa", 0),
            ns_test.reg_scope_pre("::cppmicroservicesa")
            )
        self.assertEqual(
            ("::\ncppmicroservicesa", 0),
            ns_test.reg_scope_pre("::\ncppmicroservicesa")
            )


    def test_match_all_sub_regex(self):
        """
        Test that matching still works as expected and in conjunction with each other
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        self.assertEqual(
            ("namespace mw_cppms {}", 1), 
            ns_test.sub_regex("namespace cppmicroservices {}")
            )
        self.assertEqual(
            ("namespace mw_cppms", 1), 
            ns_test.sub_regex("namespace cppmicroservices")
            )
        self.assertEqual(
            (" namespace mw_cppms {}", 1), 
            ns_test.sub_regex(" namespace cppmicroservices {}")
            )

        self.assertEqual( 
            ("code::something::ns::mw_cppms", 1), 
            ns_test.sub_regex("code::something::ns::cppmicroservices")
            )

        self.assertEqual( 
            ("namespace something = mw_cppms", 1), 
            ns_test.sub_regex("namespace something = cppmicroservices")
            )
        self.assertEqual( 
            (" namespace  somethingelse  =  mw_cppms ", 1), 
            ns_test.sub_regex(" namespace  somethingelse  =  cppmicroservices ")
            )

        self.assertEqual(
            ("std::pair<mw_cppms::blah, mw_cppms::smth> var_", 2), 
            ns_test.sub_regex("std::pair<cppmicroservices::blah, cppmicroservices::smth> var_")
            )
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ = getSomething(\"mw_cppms::res\")", 2), 
            ns_test.sub_regex("std::vector<cppmicroservices::things> var_ = getSomething(\"cppmicroservices::res\")")
            )
        self.assertEqual(
            ("std::pair<mw_cppms::blah,\nmw_cppms::smth> var_", 2), 
            ns_test.sub_regex("std::pair<cppmicroservices::blah,\ncppmicroservices::smth> var_")
            )
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms::res\")", 2), 
            ns_test.sub_regex("std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices::res\")")
            )
        self.assertEqual(
            ("mw_cppms ::  something", 1), 
            ns_test.sub_regex("cppmicroservices ::  something")
            )
        self.assertEqual(
            ("mw_cppms::something::inner", 1), 
            ns_test.sub_regex("cppmicroservices::something::inner")
            )
        
        self.assertEqual(
            (" namespace  mw_cppms  =  mw_cppms", 2), 
            ns_test.sub_regex(" namespace  cppmicroservices  =  cppmicroservices")
            )
        self.assertEqual(
            ('auto svc = std::make_shared<mw_cppms::logservice::LogServiceImpl>("mw_cppms"\n"::logservice");', 2), 
            ns_test.sub_regex('auto svc = std::make_shared<cppmicroservices::logservice::LogServiceImpl>("cppmicroservices"\n"::logservice");')
            )
        self.assertEqual(
            ('auto svc = std::make_shared<mw_cppms::logservice::LogServiceImpl>("mw_cppms " \n " ::logservice");', 2), 
            ns_test.sub_regex('auto svc = std::make_shared<cppmicroservices::logservice::LogServiceImpl>("cppmicroservices " \n " ::logservice");')
            )

        

    def test_not_match_all_sub_regex(self):
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        self.assertEqual(
            ("cppmicroservices", 0), 
            ns_test.sub_regex("cppmicroservices")
            )
        self.assertEqual(
            ('"cppmicroservices"', 0), 
            ns_test.sub_regex('"cppmicroservices"')
            )
        self.assertEqual(
            ("cppmicroservices/", 0), 
            ns_test.sub_regex("cppmicroservices/")
            )
        self.assertEqual(
            ("Cppmicroservices/", 0), 
            ns_test.sub_regex("Cppmicroservices/")
            )
        self.assertEqual(
            ("cppmicroservices/something", 0), 
            ns_test.sub_regex("cppmicroservices/something")
            )
        self.assertEqual(
            ("<cppmicroservices/something>", 0), 
            ns_test.sub_regex("<cppmicroservices/something>")
            )
        self.assertEqual(
            ('#include "cppmicroservices/BundleActivator.h"', 0), 
            ns_test.sub_regex('#include "cppmicroservices/BundleActivator.h"')
            )
        
        self.assertEqual( 
            ("std::vector<BundleResource> schemeResources = GetBundleContext().GetBundle().FindResources(\"/\", \"*.scm\", false);",0), 
            ns_test.sub_regex("std::vector<BundleResource> schemeResources = GetBundleContext().GetBundle().FindResources(\"/\", \"*.scm\", false);")
            )
        
        self.assertEqual( 
            ("namespace", 0), 
            ns_test.sub_regex("namespace")
            ) 

        self.assertEqual( 
            ("namespace test = some_namespace", 0), 
            ns_test.sub_regex("namespace test = some_namespace")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  cppmicroservicess", 0), 
            ns_test.sub_regex(" namespace  somethingelse  =  cppmicroservicess")
            )

        self.assertEqual( 
            ("using ns::some_class", 0), 
            ns_test.sub_regex("using ns::some_class")
            )
        self.assertEqual(
            ("using ccppmicroservices::thing", 0), 
            ns_test.sub_regex("using ccppmicroservices::thing")
            ) 


if __name__ == '__main__':
    unittest.main()