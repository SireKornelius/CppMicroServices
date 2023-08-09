#include <memory>
namespace cppmicroservices
{   
    struct BundleContext {};
    namespace logservice
    {
        struct LogServiceImpl {};
        namespace impl
        {
            void Start(cppmicroservices::BundleContext bc)
            {
                auto svc
                    = std::make_shared<cppmicroservices::logservice::LogServiceImpl>("cppmicroservices::logservice");
            }

            void
            Stop(cppmicroservices::BundleContext)
            {
            }
        } // namespace impl
    }     // namespace logservice
} // namespace cppmicroservices
