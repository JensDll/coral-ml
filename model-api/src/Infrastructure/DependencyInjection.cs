using Application.Data;
using Application.Data.Repositories;
using Infrastructure.Data;
using Infrastructure.Data.Repositories;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Infrastructure
{
    public static class DependencyInjection
    {
        public static void AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
        {
            services.AddSingleton<IConnectionFactory>
                (new ConnectionFactory(configuration.GetConnectionString("ModelDb")));
            services.AddSingleton<IModelRepository, ModelRepository>();
        }
    }
}
