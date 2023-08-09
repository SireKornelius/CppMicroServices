#include <memory>
namespace mw_cppms
{   
    struct BundleContext {};
    namespace logservice
    {
        struct LogServiceImpl {};
        namespace impl
        {
            void Start(mw_cppms::BundleContext bc)
            {
                auto svc
                    = std::make_shared<mw_cppms::logservice::LogServiceImpl>("mw_cppms::logservice");
            }

            void
            Stop(mw_cppms::BundleContext)
            {
            }
        } // namespace impl
    }     // namespace logservice
} // namespace mw_cppms
