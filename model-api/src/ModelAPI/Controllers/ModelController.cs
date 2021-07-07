using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Application.Data.Repositories;
using Contracts;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace ModelAPI.Controllers
{
    [ApiController]
    public class ModelController : ControllerBase
    {
        private readonly IModelRepository _modelRepository;

        public ModelController(IModelRepository modelRepository)
        {
            _modelRepository = modelRepository;
        }

        [HttpGet(ApiRoutes.Model.GetById)]
        public async Task<IActionResult> GetModelById(int id)
        {
            var model = await _modelRepository.GetById(id);

            return File(model.Model, "application/octet-stream");
        }

        [HttpPost(ApiRoutes.Model.SaveModel)]
        public async Task<IActionResult> SaveModel(IFormFile model)
        {
            int id = await _modelRepository.Save(model);

            return CreatedAtAction(nameof(SaveModel), id);
        }
    }
}
