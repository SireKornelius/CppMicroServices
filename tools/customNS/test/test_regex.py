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
    """Test that regex matching works as expected
    """

    def test_replace_namespace_declaration(self):
        """Should match (1) (2) (5) (/8) (/9)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        #match (1)
        self.assertEqual(
            ("namespace mw_cppms {}", 1), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices {}")
            )
        self.assertEqual(
            ("namespace mw_cppms", 1),
            ns_test.replace_namespace_declaration("namespace cppmicroservices")
            )
        self.assertEqual(
            (" namespace mw_cppms {}", 1), 
            ns_test.replace_namespace_declaration(" namespace cppmicroservices {}")
            )
        self.assertEqual(
            (" namespace  mw_cppms  {}", 1), 
            ns_test.replace_namespace_declaration(" namespace  cppmicroservices  {}")
            )
        self.assertEqual(
            ("namespace mw_cppms ", 1), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices ")
            )
        self.assertEqual(
            ("  namespace   mw_cppms   {", 1), 
            ns_test.replace_namespace_declaration("  namespace   cppmicroservices   {")
            )
        self.assertEqual(
            ('"namespace mw_cppms"', 1), 
            ns_test.replace_namespace_declaration('"namespace cppmicroservices"')
            )
        self.assertEqual(
            ('("namespace mw_cppms")', 1), 
            ns_test.replace_namespace_declaration('("namespace cppmicroservices")')
            )
        self.assertEqual(
            ("namespace mw_cppms { namespace mw_cppms }", 2), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices { namespace cppmicroservices }")
            )
        self.assertEqual(
            ("namespace\n mw_cppms", 1), 
            ns_test.replace_namespace_declaration("namespace\n cppmicroservices")
            )
        self.assertEqual(
            ("namespace\n\n  mw_cppms", 1), 
            ns_test.replace_namespace_declaration("namespace\n\n  cppmicroservices")
            )
        self.assertEqual(
            ("namespace  \n \n  mw_cppms", 1), 
            ns_test.replace_namespace_declaration("namespace  \n \n  cppmicroservices")
            )
        self.assertEqual(
            ("namespace \n\t mw_cppms", 1), 
            ns_test.replace_namespace_declaration("namespace \n\t cppmicroservices")
            )
        self.assertEqual(
            ("namespace \r\n mw_cppms", 1), 
            ns_test.replace_namespace_declaration("namespace \r\n cppmicroservices")
            )
        self.assertEqual(
            ('"namespace" "mw_cppms"', 1), 
            ns_test.replace_namespace_declaration('"namespace" "cppmicroservices"')
            )
        self.assertEqual(
            ('"namespace" \n\n"mw_cppms"', 1), 
            ns_test.replace_namespace_declaration('"namespace" \n\n"cppmicroservices"')
            )

        # match (2)
        self.assertEqual(
            ("inline namespace mw_cppms", 1), 
            ns_test.replace_namespace_declaration("inline namespace cppmicroservices")
            )

        # match (5)
        self.assertEqual(
            ("using namespace mw_cppms", 1), 
            ns_test.replace_namespace_declaration("using namespace cppmicroservices")
            )
        self.assertEqual(
            (" using   namespace   mw_cppms", 1), 
            ns_test.replace_namespace_declaration(" using   namespace   cppmicroservices")
            )
        self.assertEqual(
            ("using namespace mw_cppms;", 1), 
            ns_test.replace_namespace_declaration("using namespace cppmicroservices;")
            )
        self.assertEqual(
            ("using namespace mw_cppms ;", 1), 
            ns_test.replace_namespace_declaration("using namespace cppmicroservices ;")
            )
        self.assertEqual(
            ("using\nnamespace mw_cppms", 1), 
            ns_test.replace_namespace_declaration("using\nnamespace cppmicroservices")
            )
        self.assertEqual(
            ("using\nnamespace \nmw_cppms", 1), 
            ns_test.replace_namespace_declaration("using\nnamespace \ncppmicroservices")
            )
        self.assertEqual(
            ("using\nnamespace \t\n mw_cppms;", 1), 
            ns_test.replace_namespace_declaration("using\nnamespace \t\n cppmicroservices;")
            )
        # match (/8)
        self.assertEqual(
            ("namespace mw_cppms::test {}", 1), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices::test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms:: test {}", 1), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices:: test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms :: test {}", 1), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices :: test {}")
            )
        self.assertEqual(
            ("namespace \nmw_cppms\n::\ntest {}", 1), 
            ns_test.replace_namespace_declaration("namespace \ncppmicroservices\n::\ntest {}")
            )
        self.assertEqual(
            ("namespace \nmw_cppms\n ::test {}", 1), 
            ns_test.replace_namespace_declaration("namespace \ncppmicroservices\n ::test {}")
            )

        # match (/9)
        self.assertEqual(
            ("namespace mw_cppms::inline test{}", 1), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices::inline test{}")
            )
        self.assertEqual(
            ("namespace mw_cppms:: inline test {}", 1), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices:: inline test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms :: inline test {}", 1), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices :: inline test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms::\ninline test {}", 1), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices::\ninline test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms::\ninline\ntest {}", 1), 
            ns_test.replace_namespace_declaration("namespace cppmicroservices::\ninline\ntest {}")
            )
        self.assertEqual(
            ("namespace\nmw_cppms::\ninline test {}", 1), 
            ns_test.replace_namespace_declaration("namespace\ncppmicroservices::\ninline test {}")
            )

    def test_not_replace_namespace_declaration(self): 
        """Should not match (1) (2) (5) (/8) (/9)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        # not match (1)
        self.assertEqual(
            ("int temp = 3",0), 
            ns_test.replace_namespace_declaration("int temp = 3")
            )
        self.assertEqual( 
            ("std::vector<BundleResource> schemeResources = GetBundleContext().GetBundle().FindResources(\"/\", \"*.scm\", false);",0), 
            ns_test.replace_namespace_declaration("std::vector<BundleResource> schemeResources = GetBundleContext().GetBundle().FindResources(\"/\", \"*.scm\", false);")
            )

        self.assertEqual(
            ("namespace", 0), 
            ns_test.replace_namespace_declaration("namespace")
            )
        self.assertEqual(
            ("cppmicroservices", 0), 
            ns_test.replace_namespace_declaration("cppmicroservices")
            )
        self.assertEqual(
            ("namespace Cppmicroservices", 0), 
            ns_test.replace_namespace_declaration("namespace Cppmicroservices")
            )  
        self.assertEqual(
            ("code::something::namespace::cppmicroservices", 0), 
            ns_test.replace_namespace_declaration("code::something::namespace::cppmicroservices")
            )
        self.assertEqual(
            ("namespace notcppmicroservices", 0), 
            ns_test.replace_namespace_declaration("namespace notcppmicroservices")
            )
        self.assertEqual(
            ("namespace acppmicroservicesb", 0), 
            ns_test.replace_namespace_declaration("namespace acppmicroservicesb")
            )
        self.assertEqual(
            ("anamespace cppmicroservices", 0), 
            ns_test.replace_namespace_declaration("anamespace cppmicroservices")
            ) 
        self.assertEqual(
            ("namespace cppmicroservicess", 0), 
            ns_test.replace_namespace_declaration("namespace cppmicroservicess")
            )
        self.assertEqual(
            ("namespace\ncppmicroservicess", 0), 
            ns_test.replace_namespace_declaration("namespace\ncppmicroservicess")
            )
        self.assertEqual(
            (" namespace\n\n cppmicroservicess { }", 0), 
            ns_test.replace_namespace_declaration(" namespace\n\n cppmicroservicess { }")
            )
        self.assertEqual(
            ("namespace\n\tcppmicroservicess", 0), 
            ns_test.replace_namespace_declaration("namespace\n\tcppmicroservicess")
            )
        
        # not match (2)       
        self.assertEqual(
            ("inline namespace cppmicroservicess", 0), 
            ns_test.replace_namespace_declaration("inline namespace cppmicroservicess")
            )
        self.assertEqual(
            ("inline namespace\nCppmicroservices", 0), 
            ns_test.replace_namespace_declaration("inline namespace\nCppmicroservices")
            )
        self.assertEqual(
            ("inline\nnamespace\n\tCppmicroservices", 0), 
            ns_test.replace_namespace_declaration("inline\nnamespace\n\tCppmicroservices")
            )
        # not match (5)
        self.assertEqual(
            ("using namespace cppmicroservicess;", 0), 
            ns_test.replace_namespace_declaration("using namespace cppmicroservicess;")
            )
        self.assertEqual(
            ("using namespace Cppmicroservices", 0), 
            ns_test.replace_namespace_declaration("using namespace Cppmicroservices")
            )
        self.assertEqual(
            ("using namespace\ncppmicroservicess;", 0), 
            ns_test.replace_namespace_declaration("using namespace\ncppmicroservicess;")
            )
        self.assertEqual(
            ("using\nnamespace\n\nCppmicroservices", 0), 
            ns_test.replace_namespace_declaration("using\nnamespace\n\nCppmicroservices")
            )
        # not match (8)
        self.assertEqual(
            ("namespace top_namespace::test {}", 0), 
            ns_test.replace_namespace_declaration("namespace top_namespace::test {}")
            )
        self.assertEqual(
            ("namespace\ntop_namespace::test {}", 0), 
            ns_test.replace_namespace_declaration("namespace\ntop_namespace::test {}")
            )
        # not match (9)
        self.assertEqual(
            ("namespace top_namespace::inline test {}", 0), 
            ns_test.replace_namespace_declaration("namespace top_namespace::inline test {}")
            )
        self.assertEqual(
            ("namespace\ntop_namespace::inline test {}", 0), 
            ns_test.replace_namespace_declaration("namespace\ntop_namespace::inline test {}")
            )


    def test_replace_namespace_alias(self):
        """Should match (7)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        # match (7)
        self.assertEqual(
            ("namespace something = mw_cppms", 1), 
            ns_test.replace_namespace_alias("namespace something = cppmicroservices")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  mw_cppms ", 1), 
            ns_test.replace_namespace_alias(" namespace  somethingelse  =  cppmicroservices ")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  mw_cppms; ", 1), 
            ns_test.replace_namespace_alias(" namespace  somethingelse  =  cppmicroservices; ")
            )

        self.assertEqual(
            ("namespace something =\n mw_cppms", 1), 
            ns_test.replace_namespace_alias("namespace something =\n cppmicroservices")
            )
        self.assertEqual(
            (" namespace  somethingelse  \n=  mw_cppms ", 1), 
            ns_test.replace_namespace_alias(" namespace  somethingelse  \n=  cppmicroservices ")
            )
        self.assertEqual(
            (" namespace  \nsomethingelse  \n=\n  mw_cppms ", 1), 
            ns_test.replace_namespace_alias(" namespace  \nsomethingelse  \n=\n  cppmicroservices ")
            )
        self.assertEqual(
            (" namespace\n\tsomethingelse  =  mw_cppms; ", 1), 
            ns_test.replace_namespace_alias(" namespace\n\tsomethingelse  =  cppmicroservices; ")
            )
        self.assertEqual(
            ('" namespace\n\tsomethingelse" \n=  "mw_cppms; "', 1), 
            ns_test.replace_namespace_alias('" namespace\n\tsomethingelse" \n=  "cppmicroservices; "')
            )


    def test_not_replace_namespace_alias(self):
        """Should not match (7)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        self.assertEqual(
            ("cppmicroservices", 0), 
            ns_test.replace_namespace_alias("cppmicroservices")
            )
        self.assertEqual(
            ("namespace test = some_namespace", 0), 
            ns_test.replace_namespace_alias("namespace test = some_namespace")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  cppmicroservicess", 0), 
            ns_test.replace_namespace_alias(" namespace  somethingelse  =  cppmicroservicess")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  Cppmicroservices", 0), 
            ns_test.replace_namespace_alias(" namespace  somethingelse  =  Cppmicroservices")
            )
        self.assertEqual(
            (" namespace  somethingelse  \n=\n Cppmicroservices", 0), 
            ns_test.replace_namespace_alias(" namespace  somethingelse  \n=\n Cppmicroservices")
            )
        self.assertEqual(
            (" namespace\nsomethingelse  \n=\n  Cppmicroservices", 0), 
            ns_test.replace_namespace_alias(" namespace\nsomethingelse  \n=\n  Cppmicroservices")
            )
        self.assertEqual(
            ("anamespace test = cppmicroservices", 0), 
            ns_test.replace_namespace_alias("anamespace test = cppmicroservices")
            )

    def test_replace_post_namespace_resolution(self):
        """Should match (4) (6)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        # match (4)
        self.assertEqual(
            ("mw_cppms::something", 1), 
            ns_test.replace_post_namespace_resolution("cppmicroservices::something")
            )
        self.assertEqual(
            ("mw_cppms:: something", 1), 
            ns_test.replace_post_namespace_resolution("cppmicroservices:: something")
            )
        self.assertEqual(
            ("mw_cppms ::  something", 1), 
            ns_test.replace_post_namespace_resolution("cppmicroservices ::  something")
            )
        self.assertEqual(
            ("mw_cppms::something::inner", 1), 
            ns_test.replace_post_namespace_resolution("cppmicroservices::something::inner")
            )
        self.assertEqual(
            ("std::pair<mw_cppms::blah, mw_cppms::smth> var_", 2), 
            ns_test.replace_post_namespace_resolution("std::pair<cppmicroservices::blah, cppmicroservices::smth> var_")
            )
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ = getSomething(\"mw_cppms::res\")", 2), 
            ns_test.replace_post_namespace_resolution("std::vector<cppmicroservices::things> var_ = getSomething(\"cppmicroservices::res\")")
            )
        
        self.assertEqual(
            ("mw_cppms::\n\nsomething", 1), 
            ns_test.replace_post_namespace_resolution("cppmicroservices::\n\nsomething")
            )
        self.assertEqual(
            ("mw_cppms\n:: \nsomething", 1), 
            ns_test.replace_post_namespace_resolution("cppmicroservices\n:: \nsomething")
            )
        self.assertEqual(
            ("mw_cppms :: \n\tsomething", 1), 
            ns_test.replace_post_namespace_resolution("cppmicroservices :: \n\tsomething")
            )
        self.assertEqual(
            ("mw_cppms::\nsomething::\ninner", 1), 
            ns_test.replace_post_namespace_resolution("cppmicroservices::\nsomething::\ninner")
            )
        self.assertEqual(
            ("std::pair<mw_cppms::blah,\nmw_cppms::smth> var_", 2), 
            ns_test.replace_post_namespace_resolution("std::pair<cppmicroservices::blah,\ncppmicroservices::smth> var_")
            )
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms::res\")", 2), 
            ns_test.replace_post_namespace_resolution("std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices::res\")")
            )
        
        self.assertEqual(
            ("mw_cppms:: here mw_cppms::there mw_cppms::any", 3), 
            ns_test.replace_post_namespace_resolution("cppmicroservices:: here cppmicroservices::there cppmicroservices::any")
            )
        self.assertEqual(
            ("mw_cppms::here; mw_cppms::there; mw_cppms::any", 3), 
            ns_test.replace_post_namespace_resolution("cppmicroservices::here; cppmicroservices::there; cppmicroservices::any")
            )

        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms\"\"::res\")", 2), 
            ns_test.replace_post_namespace_resolution("std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices\"\"::res\")")
            )
        self.assertEqual( 
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms\"\n\"::res\")", 2), 
            ns_test.replace_post_namespace_resolution("std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices\"\n\"::res\")")
            )
        # match (6)
        self.assertEqual(
            ("using mw_cppms::some_class", 1), 
            ns_test.replace_post_namespace_resolution("using cppmicroservices::some_class")
            )
        self.assertEqual(
            ("using mw_cppms::some_class;", 1), 
            ns_test.replace_post_namespace_resolution("using cppmicroservices::some_class;")
            )
        self.assertEqual(
            ("using mw_cppms:: some_class", 1), 
            ns_test.replace_post_namespace_resolution("using cppmicroservices:: some_class")
            )
        self.assertEqual(
            ("using mw_cppms::ns::something", 1), 
            ns_test.replace_post_namespace_resolution("using cppmicroservices::ns::something")
            )
        
        self.assertEqual(
            ("using mw_cppms::\nsome_class", 1), 
            ns_test.replace_post_namespace_resolution("using cppmicroservices::\nsome_class")
            )
        self.assertEqual(
            ("using\nmw_cppms\n::\nsome_class;", 1), 
            ns_test.replace_post_namespace_resolution("using\ncppmicroservices\n::\nsome_class;")
            )
        self.assertEqual(
            ("using mw_cppms::\n\t some_class", 1), 
            ns_test.replace_post_namespace_resolution("using cppmicroservices::\n\t some_class")
            )
        self.assertEqual(
            ("using mw_cppms::\nns::\nsomething", 1), 
            ns_test.replace_post_namespace_resolution("using cppmicroservices::\nns::\nsomething")
            )

    def test_not_replace_post_namespace_resolution(self):
        """Should not match (4) (6)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        # not match (4)
        self.assertEqual(
            ("int temp = 3", 0), 
            ns_test.replace_post_namespace_resolution("int temp = 3")
            )
        self.assertEqual(
            ("<cppmicroservices>", 0), 
            ns_test.replace_post_namespace_resolution("<cppmicroservices>")
            )
        self.assertEqual(
            ("cppmicroservices", 0), 
            ns_test.replace_post_namespace_resolution("cppmicroservices")
            )
        self.assertEqual(
            ("ccppmicroservices::something", 0), 
            ns_test.replace_post_namespace_resolution("ccppmicroservices::something")
            )
        self.assertEqual(
            ("cppmicroservicess::\nsomething", 0), 
            ns_test.replace_post_namespace_resolution("cppmicroservicess::\nsomething")
            )
        self.assertEqual(
            ("cppmicroservicess::\n\nsomething", 0), 
            ns_test.replace_post_namespace_resolution("cppmicroservicess::\n\nsomething")
            )
        self.assertEqual(
            ("cppmicroservicess::\n\n\tsomething", 0), 
            ns_test.replace_post_namespace_resolution("cppmicroservicess::\n\n\tsomething")
            )
        self.assertEqual(
            ("cppmicroservices'::something", 0), 
            ns_test.replace_post_namespace_resolution("cppmicroservices'::something")
            )
        self.assertEqual(
            ("Cppmicroservices::something", 0), 
            ns_test.replace_post_namespace_resolution("Cppmicroservices::something"))

        # not match (6)
        self.assertEqual(
            ("using ns::some_class", 0), 
            ns_test.replace_post_namespace_resolution("using ns::some_class")
            )
        self.assertEqual(
            ("using ccppmicroservices::thing", 0), 
            ns_test.replace_post_namespace_resolution("using ccppmicroservices::thing")
            ) 
        self.assertEqual(
            ("using Cppmicroservices::thing", 0), 
            ns_test.replace_post_namespace_resolution("using Cppmicroservices::thing")
            )     

        self.assertEqual(
            ("using\nns::some_class", 0), 
            ns_test.replace_post_namespace_resolution("using\nns::some_class")
            )
        self.assertEqual(
            ("using ccppmicroservices\n::thing", 0), 
            ns_test.replace_post_namespace_resolution("using ccppmicroservices\n::thing")
            ) 
        self.assertEqual(
            ("using\nCppmicroservices\n::\nthing", 0), 
            ns_test.replace_post_namespace_resolution("using\nCppmicroservices\n::\nthing")
            )       

    def test_replace_pre_namespace_resolution(self):
        """Match edge cases (/8) (/9)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        self.assertEqual(
            ("namespace foo::inline mw_cppms{}", 1), 
            ns_test.replace_pre_namespace_resolution("namespace foo::inline cppmicroservices{}")
            )  
        self.assertEqual(
            ("namespace foo:: \ninline mw_cppms{}", 1), 
            ns_test.replace_pre_namespace_resolution("namespace foo:: \ninline cppmicroservices{}")
            )   
        self.assertEqual(
            ("namespace foo::mw_cppms{}", 1), 
            ns_test.replace_pre_namespace_resolution("namespace foo::cppmicroservices{}")
            )  
        self.assertEqual(
            ("namespace foo::\nmw_cppms{}", 1), 
            ns_test.replace_pre_namespace_resolution("namespace foo::\ncppmicroservices{}")
            )  
        self.assertEqual(
            ("using namespace ::mw_cppms", 1), 
            ns_test.replace_pre_namespace_resolution("using namespace ::cppmicroservices")
            )  
        self.assertEqual(
            ("using namespace ::\nmw_cppms", 1), 
            ns_test.replace_pre_namespace_resolution("using namespace ::\ncppmicroservices")
            )  
        self.assertEqual(
            ('"using namespace ::mw_cppms"', 1), 
            ns_test.replace_pre_namespace_resolution('"using namespace ::cppmicroservices"')
            )   
        self.assertEqual(
            ("using   ::mw_cppms", 1), 
            ns_test.replace_pre_namespace_resolution("using   ::cppmicroservices")
            )
        self.assertEqual(
            ('"using" "::mw_cppms"', 1), 
            ns_test.replace_pre_namespace_resolution('"using" "::cppmicroservices"')
            )       
        self.assertEqual(
            ("::mw_cppms", 1), 
            ns_test.replace_pre_namespace_resolution("::cppmicroservices")
            )    
        self.assertEqual(
            (":: mw_cppms", 1), 
            ns_test.replace_pre_namespace_resolution(":: cppmicroservices")
            )
        self.assertEqual(
            ("::mw_cppms", 1), 
            ns_test.replace_pre_namespace_resolution("::cppmicroservices")
            )

    def test_not_replace_pre_namespace_resolution(self):
        """Not match edge cases (/8) (/9)
        """
        ns_test = NamespaceModifier('cppmicroservices', 'mw_cppms')
        self.assertEqual(
            ("cppmicroservices", 0), 
            ns_test.replace_pre_namespace_resolution("cppmicroservices")
            )
        self.assertEqual(
            ("random::something()", 0),
            ns_test.replace_pre_namespace_resolution("random::something()")
            )
        self.assertEqual(
            ("::cppmicroservicesa", 0),
            ns_test.replace_pre_namespace_resolution("::cppmicroservicesa")
            )
        self.assertEqual(
            ("::\ncppmicroservicesa", 0),
            ns_test.replace_pre_namespace_resolution("::\ncppmicroservicesa")
            )

    def test_sub_regex(self):
        """Testing matching namespace usage works as expected
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

    def test_not_sub_regex(self):
        """Testing non-namespace usages are not matched
        """
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