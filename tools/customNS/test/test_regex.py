import unittest
from src.utils import reg_name_dec, reg_alias_name, reg_scope_post, sub_regex, reg_scope_pre

''' All usages of namespaces according to cppreferences
namespace ns-name { declarations }	(1)	
inline namespace ns-name { declarations }	(2)	(since C++11)
namespace { declarations }	(3)
ns-name :: member-name	(4)	
using namespace ns-name ;	(5)	
using ns-name :: member-name ;	(6)	
namespace name = qualified-namespace ;	(7)	
namespace ns-name :: member-name { declarations }	(8)	(since C++17)
namespace ns-name :: inline member-name { declarations }	(9)	(since C++20)
'''

class TestRegex(unittest.TestCase):

    def test_match_reg_name_dec(self): #added whitespace tests
        '''
        Should match (1) (2) (5) (/8) (/9)
        '''
        # (1)
        self.assertEqual(
            ("namespace mw_cppms {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices {}")
            )
        self.assertEqual(
            ("namespace mw_cppms", 1),
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices")
            )
        self.assertEqual(
            (" namespace mw_cppms {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", " namespace cppmicroservices {}")
            )
        self.assertEqual(
            (" namespace  mw_cppms  {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", " namespace  cppmicroservices  {}")
            )
        self.assertEqual(
            ("namespace mw_cppms ", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices ")
            )
        self.assertEqual(
            ("  namespace   mw_cppms   {", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "  namespace   cppmicroservices   {")
            )
        self.assertEqual(
            ('"namespace mw_cppms"', 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", '"namespace cppmicroservices"')
            )
        self.assertEqual(
            ('("namespace mw_cppms")', 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", '("namespace cppmicroservices")')
            )
        self.assertEqual(
            ("namespace mw_cppms { namespace mw_cppms }", 2), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices { namespace cppmicroservices }")
            )
        self.assertEqual(
            ("namespace\n mw_cppms", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace\n cppmicroservices")
            )
        self.assertEqual(
            ("namespace\n\n  mw_cppms", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace\n\n  cppmicroservices")
            )
        self.assertEqual(
            ("namespace  \n \n  mw_cppms", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace  \n \n  cppmicroservices")
            )
        self.assertEqual(
            ("namespace \n\t mw_cppms", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace \n\t cppmicroservices")
            )
        self.assertEqual(
            ("namespace \r\n mw_cppms", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace \r\n cppmicroservices")
            )
        self.assertEqual(
            ('"namespace" "mw_cppms"', 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", '"namespace" "cppmicroservices"')
            )
        self.assertEqual(
            ('"namespace" \n\n"mw_cppms"', 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", '"namespace" \n\n"cppmicroservices"')
            )

        #2
        self.assertEqual(
            ("inline namespace mw_cppms", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "inline namespace cppmicroservices")
            )

        #5
        self.assertEqual(
            ("using namespace mw_cppms", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "using namespace cppmicroservices")
            )
        self.assertEqual(
            (" using   namespace   mw_cppms", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", " using   namespace   cppmicroservices")
            )
        self.assertEqual(
            ("using namespace mw_cppms;", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "using namespace cppmicroservices;")
            )
        self.assertEqual(
            ("using namespace mw_cppms ;", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "using namespace cppmicroservices ;")
            )
        self.assertEqual(
            ("using\nnamespace mw_cppms", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "using\nnamespace cppmicroservices")
            )
        self.assertEqual(
            ("using\nnamespace \nmw_cppms", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "using\nnamespace \ncppmicroservices")
            )
        self.assertEqual(
            ("using\nnamespace \t\n mw_cppms;", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "using\nnamespace \t\n cppmicroservices;")
            )
        #8
        self.assertEqual(
            ("namespace mw_cppms::test {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices::test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms:: test {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices:: test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms :: test {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices :: test {}")
            )
        self.assertEqual(
            ("namespace \nmw_cppms\n::\ntest {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace \ncppmicroservices\n::\ntest {}")
            )
        self.assertEqual(
            ("namespace \nmw_cppms\n ::test {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace \ncppmicroservices\n ::test {}")
            )

        #9
        self.assertEqual(
            ("namespace mw_cppms::inline test{}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices::inline test{}")
            )
        self.assertEqual(
            ("namespace mw_cppms:: inline test {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices:: inline test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms :: inline test {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices :: inline test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms::\ninline test {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices::\ninline test {}")
            )
        self.assertEqual(
            ("namespace mw_cppms::\ninline\ntest {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservices::\ninline\ntest {}")
            )
        self.assertEqual(
            ("namespace\nmw_cppms::\ninline test {}", 1), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace\ncppmicroservices::\ninline test {}")
            )


    def test_not_match_reg_name_dec(self): 
        '''
        Should not match
        '''
        # (1)
        self.assertEqual(
            ("int temp = 3",0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "int temp = 3")
            )
        self.assertEqual( 
            ("std::vector<BundleResource> schemeResources = GetBundleContext().GetBundle().FindResources(\"/\", \"*.scm\", false);",0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "std::vector<BundleResource> schemeResources = GetBundleContext().GetBundle().FindResources(\"/\", \"*.scm\", false);")
            )

        self.assertEqual(
            ("namespace", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace")
            )
        self.assertEqual(
            ("cppmicroservices", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "cppmicroservices")
            )
        self.assertEqual(
            ("namespace Cppmicroservices", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace Cppmicroservices")
            )  
        self.assertEqual(
            ("code::something::namespace::cppmicroservices", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "code::something::namespace::cppmicroservices")
            )
        self.assertEqual(
            ("namespace notcppmicroservices", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace notcppmicroservices")
            )
        self.assertEqual(
            ("namespace acppmicroservicesb", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace acppmicroservicesb")
            )
        self.assertEqual(
            ("anamespace cppmicroservices", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "anamespace cppmicroservices")
            ) 
        self.assertEqual(
            ("namespace cppmicroservicess", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace cppmicroservicess")
            )
        self.assertEqual(
            ("namespace\ncppmicroservicess", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace\ncppmicroservicess")
            )
        self.assertEqual(
            (" namespace\n\n cppmicroservicess { }", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", " namespace\n\n cppmicroservicess { }")
            )
        self.assertEqual(
            ("namespace\n\tcppmicroservicess", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace\n\tcppmicroservicess")
            )
        
        # (2)       
        self.assertEqual(
            ("inline namespace cppmicroservicess", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "inline namespace cppmicroservicess")
            )
        self.assertEqual(
            ("inline namespace\nCppmicroservices", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "inline namespace\nCppmicroservices")
            )
        self.assertEqual(
            ("inline\nnamespace\n\tCppmicroservices", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "inline\nnamespace\n\tCppmicroservices")
            )
        # (5)
        self.assertEqual(
            ("using namespace cppmicroservicess;", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "using namespace cppmicroservicess;")
            )
        self.assertEqual(
            ("using namespace Cppmicroservices", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "using namespace Cppmicroservices")
            )
        self.assertEqual(
            ("using namespace\ncppmicroservicess;", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "using namespace\ncppmicroservicess;")
            )
        self.assertEqual(
            ("using\nnamespace\n\nCppmicroservices", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "using\nnamespace\n\nCppmicroservices")
            )
        # (8)
        self.assertEqual(
            ("namespace top_namespace::test {}", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace top_namespace::test {}")
            )
        self.assertEqual(
            ("namespace\ntop_namespace::test {}", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace\ntop_namespace::test {}")
            )
        # (9)
        self.assertEqual(
            ("namespace top_namespace::inline test {}", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace top_namespace::inline test {}")
            )
        self.assertEqual(
            ("namespace\ntop_namespace::inline test {}", 0), 
            reg_name_dec("cppmicroservices", "mw_cppms", "namespace\ntop_namespace::inline test {}")
            )


    def test_match_reg_alias_name(self):
        '''
        Should match (7)
        '''
        # (7)
        self.assertEqual(
            ("namespace something = mw_cppms", 1), 
            reg_alias_name("cppmicroservices", "mw_cppms", "namespace something = cppmicroservices")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  mw_cppms ", 1), 
            reg_alias_name("cppmicroservices", "mw_cppms", " namespace  somethingelse  =  cppmicroservices ")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  mw_cppms; ", 1), 
            reg_alias_name("cppmicroservices", "mw_cppms", " namespace  somethingelse  =  cppmicroservices; ")
            )

        self.assertEqual(
            ("namespace something =\n mw_cppms", 1), 
            reg_alias_name("cppmicroservices", "mw_cppms", "namespace something =\n cppmicroservices")
            )
        self.assertEqual(
            (" namespace  somethingelse  \n=  mw_cppms ", 1), 
            reg_alias_name("cppmicroservices", "mw_cppms", " namespace  somethingelse  \n=  cppmicroservices ")
            )
        self.assertEqual(
            (" namespace  \nsomethingelse  \n=\n  mw_cppms ", 1), 
            reg_alias_name("cppmicroservices", "mw_cppms", " namespace  \nsomethingelse  \n=\n  cppmicroservices ")
            )
        self.assertEqual(
            (" namespace\n\tsomethingelse  =  mw_cppms; ", 1), 
            reg_alias_name("cppmicroservices", "mw_cppms", " namespace\n\tsomethingelse  =  cppmicroservices; ")
            )
        self.assertEqual(
            ('" namespace\n\tsomethingelse" \n=  "mw_cppms; "', 1), 
            reg_alias_name("cppmicroservices", "mw_cppms", '" namespace\n\tsomethingelse" \n=  "cppmicroservices; "')
            )


    def test_not_match_reg_alias_name(self):
        # (7)
        self.assertEqual(
            ("cppmicroservices", 0), 
            reg_alias_name("cppmicroservices", "mw_cppms", "cppmicroservices")
            )
        self.assertEqual(
            ("namespace test = some_namespace", 0), 
            reg_alias_name("cppmicroservices", "mw_cppms", "namespace test = some_namespace")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  cppmicroservicess", 0), 
            reg_alias_name("cppmicroservices", "mw_cppms", " namespace  somethingelse  =  cppmicroservicess")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  Cppmicroservices", 0), 
            reg_alias_name("cppmicroservices", "mw_cppms", " namespace  somethingelse  =  Cppmicroservices")
            )
        self.assertEqual(
            (" namespace  somethingelse  \n=\n Cppmicroservices", 0), 
            reg_alias_name("cppmicroservices", "mw_cppms", " namespace  somethingelse  \n=\n Cppmicroservices")
            )
        self.assertEqual(
            (" namespace\nsomethingelse  \n=\n  Cppmicroservices", 0), 
            reg_alias_name("cppmicroservices", "mw_cppms", " namespace\nsomethingelse  \n=\n  Cppmicroservices")
            )
        self.assertEqual(
            ("anamespace test = cppmicroservices", 0), 
            reg_alias_name("cppmicroservices", "mw_cppms", "anamespace test = cppmicroservices")
            )

    def test_match_reg_scope_post(self):
        '''
        (4) (6)
        '''
        # (4)
        self.assertEqual(
            ("mw_cppms::something", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices::something")
            )
        self.assertEqual(
            ("mw_cppms:: something", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices:: something")
            )
        self.assertEqual(
            ("mw_cppms ::  something", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices ::  something")
            )
        self.assertEqual(
            ("mw_cppms::something::inner", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices::something::inner")
            )
        self.assertEqual(
            ("std::pair<mw_cppms::blah, mw_cppms::smth> var_", 2), 
            reg_scope_post("cppmicroservices", "mw_cppms", "std::pair<cppmicroservices::blah, cppmicroservices::smth> var_")
            )
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ = getSomething(\"mw_cppms::res\")", 2), 
            reg_scope_post("cppmicroservices", "mw_cppms", "std::vector<cppmicroservices::things> var_ = getSomething(\"cppmicroservices::res\")")
            )
        
        self.assertEqual(
            ("mw_cppms::\n\nsomething", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices::\n\nsomething")
            )
        self.assertEqual(
            ("mw_cppms\n:: \nsomething", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices\n:: \nsomething")
            )
        self.assertEqual(
            ("mw_cppms :: \n\tsomething", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices :: \n\tsomething")
            )
        self.assertEqual(
            ("mw_cppms::\nsomething::\ninner", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices::\nsomething::\ninner")
            )
        self.assertEqual(
            ("std::pair<mw_cppms::blah,\nmw_cppms::smth> var_", 2), 
            reg_scope_post("cppmicroservices", "mw_cppms", "std::pair<cppmicroservices::blah,\ncppmicroservices::smth> var_")
            )
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms::res\")", 2), 
            reg_scope_post("cppmicroservices", "mw_cppms", "std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices::res\")")
            )
        
        self.assertEqual(
            ("mw_cppms:: here mw_cppms::there mw_cppms::any", 3), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices:: here cppmicroservices::there cppmicroservices::any")
            )
        self.assertEqual(
            ("mw_cppms::here; mw_cppms::there; mw_cppms::any", 3), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices::here; cppmicroservices::there; cppmicroservices::any")
            )

        # split in strings.
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms\"\"::res\")", 2), 
            reg_scope_post("cppmicroservices", "mw_cppms", "std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices\"\"::res\")")
            )
        self.assertEqual( 
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms\"\n\"::res\")", 2), 
            reg_scope_post("cppmicroservices", "mw_cppms", "std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices\"\n\"::res\")")
            )
        # (7)
        self.assertEqual(
            ("using mw_cppms::some_class", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using cppmicroservices::some_class")
            )
        self.assertEqual(
            ("using mw_cppms::some_class;", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using cppmicroservices::some_class;")
            )
        self.assertEqual(
            ("using mw_cppms:: some_class", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using cppmicroservices:: some_class")
            )
        self.assertEqual(
            ("using mw_cppms::ns::something", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using cppmicroservices::ns::something")
            )
        
        self.assertEqual(
            ("using mw_cppms::\nsome_class", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using cppmicroservices::\nsome_class")
            )
        self.assertEqual(
            ("using\nmw_cppms\n::\nsome_class;", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using\ncppmicroservices\n::\nsome_class;")
            )
        self.assertEqual(
            ("using mw_cppms::\n\t some_class", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using cppmicroservices::\n\t some_class")
            )
        self.assertEqual(
            ("using mw_cppms::\nns::\nsomething", 1), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using cppmicroservices::\nns::\nsomething")
            )


    def test_not_match_reg_scope_post(self):
        # (4)
        self.assertEqual(
            ("int temp = 3", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "int temp = 3")
            )
        self.assertEqual(
            ("<cppmicroservices>", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "<cppmicroservices>")
            )
        self.assertEqual(
            ("cppmicroservices", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices")
            )
        self.assertEqual(
            ("ccppmicroservices::something", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "ccppmicroservices::something")
            )
        self.assertEqual(
            ("cppmicroservicess::\nsomething", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservicess::\nsomething")
            )
        self.assertEqual(
            ("cppmicroservicess::\n\nsomething", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservicess::\n\nsomething")
            )
        self.assertEqual(
            ("cppmicroservicess::\n\n\tsomething", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservicess::\n\n\tsomething")
            )
        self.assertEqual(
            ("cppmicroservices'::something", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "cppmicroservices'::something")
            )
        self.assertEqual(
            ("Cppmicroservices::something", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "Cppmicroservices::something"))

        # (7)
        self.assertEqual(
            ("using ns::some_class", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using ns::some_class")
            )
        self.assertEqual(
            ("using ccppmicroservices::thing", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using ccppmicroservices::thing")
            ) 
        self.assertEqual(
            ("using Cppmicroservices::thing", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using Cppmicroservices::thing")
            )     

        self.assertEqual(
            ("using\nns::some_class", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using\nns::some_class")
            )
        self.assertEqual(
            ("using ccppmicroservices\n::thing", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using ccppmicroservices\n::thing")
            ) 
        self.assertEqual(
            ("using\nCppmicroservices\n::\nthing", 0), 
            reg_scope_post("cppmicroservices", "mw_cppms", "using\nCppmicroservices\n::\nthing")
            )       


    def test_match_reg_scope_pre(self):
        '''
        (/8) (/9)
        '''
        self.assertEqual(
            ("namespace foo::inline mw_cppms{}", 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", "namespace foo::inline cppmicroservices{}")
            )  
        self.assertEqual(
            ("namespace foo:: \ninline mw_cppms{}", 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", "namespace foo:: \ninline cppmicroservices{}")
            )   
        self.assertEqual(
            ("namespace foo::mw_cppms{}", 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", "namespace foo::cppmicroservices{}")
            )  
        self.assertEqual(
            ("namespace foo::\nmw_cppms{}", 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", "namespace foo::\ncppmicroservices{}")
            )  
        self.assertEqual(
            ("using namespace ::mw_cppms", 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", "using namespace ::cppmicroservices")
            )  
        self.assertEqual(
            ("using namespace ::\nmw_cppms", 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", "using namespace ::\ncppmicroservices")
            )  
        self.assertEqual(
            ('"using namespace ::mw_cppms"', 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", '"using namespace ::cppmicroservices"')
            )   
        self.assertEqual(
            ("using   ::mw_cppms", 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", "using   ::cppmicroservices")
            )
        self.assertEqual(
            ('"using" "::mw_cppms"', 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", '"using" "::cppmicroservices"')
            )       
        self.assertEqual(
            ("::mw_cppms", 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", "::cppmicroservices")
            )    
        self.assertEqual(
            (":: mw_cppms", 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", ":: cppmicroservices")
            )
        self.assertEqual(
            ("::mw_cppms", 1), 
            reg_scope_pre("cppmicroservices", "mw_cppms", "::cppmicroservices")
            )

    def test_not_match_reg_scope_pre(self):
        self.assertEqual(
            ("cppmicroservices", 0), 
            reg_scope_pre("cppmicroservices", "mw_cppms", "cppmicroservices")
            )
        self.assertEqual(
            ("random::something()", 0),
            reg_scope_pre("cppmicroservices", "mw_cppms", "random::something()")
            )
        self.assertEqual(
            ("::cppmicroservicesa", 0),
            reg_scope_pre("cppmicroservices", "mw_cppms", "::cppmicroservicesa")
            )
        self.assertEqual(
            ("::\ncppmicroservicesa", 0),
            reg_scope_pre("cppmicroservices", "mw_cppms", "::\ncppmicroservicesa")
            )


    def test_match_all_sub_regex(self):
        '''
        Test that matching still works as expected and in conjunction with each other
        '''
        self.assertEqual(
            ("namespace mw_cppms {}", 1), 
            sub_regex("cppmicroservices", "mw_cppms", "namespace cppmicroservices {}")
            )
        self.assertEqual(
            ("namespace mw_cppms", 1), 
            sub_regex("cppmicroservices", "mw_cppms", "namespace cppmicroservices")
            )
        self.assertEqual(
            (" namespace mw_cppms {}", 1), 
            sub_regex("cppmicroservices", "mw_cppms", " namespace cppmicroservices {}")
            )

        self.assertEqual( 
            ("code::something::ns::mw_cppms", 1), 
            sub_regex("cppmicroservices", "mw_cppms", "code::something::ns::cppmicroservices")
            )

        self.assertEqual( 
            ("namespace something = mw_cppms", 1), 
            sub_regex("cppmicroservices", "mw_cppms", "namespace something = cppmicroservices")
            )
        self.assertEqual( 
            (" namespace  somethingelse  =  mw_cppms ", 1), 
            sub_regex("cppmicroservices", "mw_cppms", " namespace  somethingelse  =  cppmicroservices ")
            )

        self.assertEqual(
            ("std::pair<mw_cppms::blah, mw_cppms::smth> var_", 2), 
            sub_regex("cppmicroservices", "mw_cppms", "std::pair<cppmicroservices::blah, cppmicroservices::smth> var_")
            )
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ = getSomething(\"mw_cppms::res\")", 2), 
            sub_regex("cppmicroservices", "mw_cppms", "std::vector<cppmicroservices::things> var_ = getSomething(\"cppmicroservices::res\")")
            )
        self.assertEqual(
            ("std::pair<mw_cppms::blah,\nmw_cppms::smth> var_", 2), 
            sub_regex("cppmicroservices", "mw_cppms", "std::pair<cppmicroservices::blah,\ncppmicroservices::smth> var_")
            )
        self.assertEqual(
            ("std::vector<mw_cppms::things> var_ =\n getSomething(\"mw_cppms::res\")", 2), 
            sub_regex("cppmicroservices", "mw_cppms", "std::vector<cppmicroservices::things> var_ =\n getSomething(\"cppmicroservices::res\")")
            )
        self.assertEqual(
            ("mw_cppms ::  something", 1), 
            sub_regex("cppmicroservices", "mw_cppms", "cppmicroservices ::  something")
            )
        self.assertEqual(
            ("mw_cppms::something::inner", 1), 
            sub_regex("cppmicroservices", "mw_cppms", "cppmicroservices::something::inner")
            )
        
        self.assertEqual(
            (" namespace  mw_cppms  =  mw_cppms", 2), 
            sub_regex("cppmicroservices", "mw_cppms", " namespace  cppmicroservices  =  cppmicroservices")
            )
        self.assertEqual(
            ('auto svc = std::make_shared<mw_cppms::logservice::LogServiceImpl>("mw_cppms"\n"::logservice");', 2), 
            sub_regex("cppmicroservices", "mw_cppms", 'auto svc = std::make_shared<cppmicroservices::logservice::LogServiceImpl>("cppmicroservices"\n"::logservice");')
            )
        self.assertEqual(
            ('auto svc = std::make_shared<mw_cppms::logservice::LogServiceImpl>("mw_cppms " \n " ::logservice");', 2), 
            sub_regex("cppmicroservices", "mw_cppms", 'auto svc = std::make_shared<cppmicroservices::logservice::LogServiceImpl>("cppmicroservices " \n " ::logservice");')
            )

        

    def test_not_match_all_sub_regex(self):
        self.assertEqual(
            ("cppmicroservices", 0), 
            sub_regex("cppmicroservices", "mw_cppms", "cppmicroservices")
            )
        self.assertEqual(
            ('"cppmicroservices"', 0), 
            sub_regex("cppmicroservices", "mw_cppms", '"cppmicroservices"')
            )
        self.assertEqual(
            ("cppmicroservices/", 0), 
            sub_regex("cppmicroservices", "mw_cppms", "cppmicroservices/")
            )
        self.assertEqual(
            ("Cppmicroservices/", 0), 
            sub_regex("cppmicroservices", "mw_cppms", "Cppmicroservices/")
            )
        self.assertEqual(
            ("cppmicroservices/something", 0), 
            sub_regex("cppmicroservices", "mw_cppms", "cppmicroservices/something")
            )
        self.assertEqual(
            ("<cppmicroservices/something>", 0), 
            sub_regex("cppmicroservices", "mw_cppms", "<cppmicroservices/something>")
            )
        self.assertEqual(
            ('#include "cppmicroservices/BundleActivator.h"', 0), 
            sub_regex("cppmicroservices", "mw_cppms", '#include "cppmicroservices/BundleActivator.h"')
            )
        
        self.assertEqual( 
            ("std::vector<BundleResource> schemeResources = GetBundleContext().GetBundle().FindResources(\"/\", \"*.scm\", false);",0), 
            sub_regex("cppmicroservices", "mw_cppms", "std::vector<BundleResource> schemeResources = GetBundleContext().GetBundle().FindResources(\"/\", \"*.scm\", false);")
            )
        
        self.assertEqual( 
            ("namespace", 0), 
            sub_regex("cppmicroservices", "mw_cppms", "namespace")
            ) 

        self.assertEqual( 
            ("namespace test = some_namespace", 0), 
            sub_regex("cppmicroservices", "mw_cppms", "namespace test = some_namespace")
            )
        self.assertEqual(
            (" namespace  somethingelse  =  cppmicroservicess", 0), 
            sub_regex("cppmicroservices", "mw_cppms", " namespace  somethingelse  =  cppmicroservicess")
            )

        self.assertEqual( 
            ("using ns::some_class", 0), 
            sub_regex("cppmicroservices", "mw_cppms", "using ns::some_class")
            )
        self.assertEqual(
            ("using ccppmicroservices::thing", 0), 
            sub_regex("cppmicroservices", "mw_cppms", "using ccppmicroservices::thing")
            ) 


if __name__ == '__main__':
    unittest.main()