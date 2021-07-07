using Application.Data.Models;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Data.Repositories
{
    public interface IModelRepository
    {

        public Task<int> Save(IFormFile model);

        public Task<TFLiteModelModel> GetById(int id);

        public Task<byte[]> GetAll();
    }
}
